package example.oneuimods

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.os.PatternMatcher
import androidx.core.content.ContextCompat
import dalvik.system.PathClassLoader
import java.io.File
import java.security.MessageDigest
import java.util.concurrent.LinkedBlockingQueue
import java.util.concurrent.ThreadPoolExecutor
import java.util.concurrent.TimeUnit

/**
 * Loads a replaceable implementation from this module's installed release APK.
 * Keep the interface and any values crossing it outside the implementation namespace.
 */
internal class SignedLogic<T : Any>(
    private val packageName: String,
    initialVersion: Long,
    private val signer: String,
    private val contract: Class<T>,
    private val entry: String,
    private val bundled: T,
    private val accepts: (T) -> Boolean,
    private val report: (String) -> Unit,
) {
    private val prefix = entry.substringBeforeLast('.') + "."
    private val worker by lazy {
        ThreadPoolExecutor(1, 1, 15, TimeUnit.SECONDS, LinkedBlockingQueue<Runnable>()) {
            task -> Thread(task, "OneUiModsLiveLogic").apply { isDaemon = true }
        }.apply { allowCoreThreadTimeOut(true) }
    }
    private var examined = initialVersion
    data class Snapshot<T>(val generation: Long, val logic: T)

    @Volatile var current = Snapshot(0, bundled)
        private set
    private var watching = false

    @Synchronized
    fun start(host: Context) {
        if (watching) return
        val app = host.applicationContext ?: host
        val filter = IntentFilter(Intent.ACTION_PACKAGE_REPLACED).apply {
            addDataScheme("package")
            addDataSchemeSpecificPart(packageName, PatternMatcher.PATTERN_LITERAL)
        }
        val receiver = object : BroadcastReceiver() {
            override fun onReceive(context: Context, intent: Intent) {
                if (intent.action == Intent.ACTION_PACKAGE_REPLACED &&
                    intent.data?.schemeSpecificPart == packageName) worker.execute { update(app) }
            }
        }
        try {
            ContextCompat.registerReceiver(app, receiver, filter, ContextCompat.RECEIVER_EXPORTED)
            watching = true
            worker.execute { update(app) }
        } catch (error: RuntimeException) {
            report("LIVE_LOGIC_WATCH_FAILED ${error.javaClass.simpleName}")
        }
    }

    @Synchronized
    fun reject(failed: Snapshot<T>, error: Throwable) {
        if (current !== failed || failed.logic === bundled) return
        current = Snapshot(failed.generation + 1, bundled)
        report("LIVE_LOGIC_FALLBACK ${error.javaClass.simpleName}")
    }

    private fun update(app: Context) {
        try {
            val apk = read(app)
            if (apk.version <= examined) return
            val loader = LogicLoader(apk.path, checkNotNull(contract.classLoader))
            val replacement = loader.loadClass(entry).asSubclass(contract)
                .getDeclaredConstructor().newInstance()
            check(accepts(replacement)) { "Incompatible live logic contract" }
            if (apk != read(app)) return
            examined = apk.version
            synchronized(this) { current = Snapshot(current.generation + 1, replacement) }
            report("ONEUI_MODS_HOT_RELOAD package=$packageName version=${apk.version} pid=${android.os.Process.myPid()}")
        } catch (error: Exception) {
            report("LIVE_LOGIC_REJECTED ${error.javaClass.simpleName}")
        } catch (error: LinkageError) {
            report("LIVE_LOGIC_REJECTED ${error.javaClass.simpleName}")
        }
    }

    private data class Installed(val version: Long, val path: String)

    @Suppress("DEPRECATION")
    private fun read(app: Context): Installed {
        val info = app.packageManager.getPackageInfo(packageName, PackageManager.GET_SIGNING_CERTIFICATES)
        val certificate = checkNotNull(info.signingInfo?.apkContentsSigners?.singleOrNull())
        val digest = MessageDigest.getInstance("SHA-256").digest(certificate.toByteArray())
            .joinToString("") { (it.toInt() and 255).toString(16).padStart(2, '0') }
        check(digest == signer) { "Installed APK signer changed" }
        val path = checkNotNull(info.applicationInfo?.sourceDir)
        val file = File(path)
        check(path.startsWith("/data/app/") && file.isFile && file.name == "base.apk" &&
            file.canonicalPath == path)
        return Installed(info.longVersionCode, path)
    }

    private inner class LogicLoader(path: String, parent: ClassLoader) : PathClassLoader(path, parent) {
        @Synchronized
        override fun loadClass(name: String, resolve: Boolean): Class<*> {
            if (!name.startsWith(prefix)) return super.loadClass(name, resolve)
            val type = findLoadedClass(name) ?: findClass(name)
            if (resolve) resolveClass(type)
            return type
        }
    }
}
