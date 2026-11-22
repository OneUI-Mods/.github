package example.oneuimods

import android.os.Process
import android.util.Log
import io.github.libxposed.api.XposedInterface.ExceptionMode
import io.github.libxposed.api.XposedModule
import io.github.libxposed.api.XposedModuleInterface.HotReloadedParam
import io.github.libxposed.api.XposedModuleInterface.HotReloadingParam
import io.github.libxposed.api.XposedModuleInterface.PackageReadyParam

/** Example for a module whose hook owns no observers, workers, or native references. */
class HookEntry : XposedModule() {
    @Volatile private var hostLoader: ClassLoader? = null

    override fun onPackageReady(param: PackageReadyParam) {
        if (param.isFirstPackage && param.packageName == TARGET && android.app.Application.getProcessName() == TARGET) {
            install(param.classLoader)
        }
    }

    override fun onHotReloading(param: HotReloadingParam): Boolean {
        val loader = hostLoader ?: return false
        param.setSavedInstanceState(loader)
        return true
    }

    override fun onHotReloaded(param: HotReloadedParam) {
        val loader = param.savedInstanceState as? ClassLoader ?: return
        if (param.processName != TARGET) return
        install(loader)
        param.oldHookHandles.forEach { it.unhook() }
        val version = BuildConfig.VERSION_CODE
        Log.i("Example", "ONEUI_MODS_HOT_RELOAD package=${BuildConfig.APPLICATION_ID} version=$version pid=${Process.myPid()}")
    }

    private fun install(loader: ClassLoader) {
        val owner = loader.loadClass("$TARGET.StockView")
        val method = owner.getDeclaredMethod("render")
        hook(method).setId("stock-view-render").setExceptionMode(ExceptionMode.PROTECTIVE)
            .intercept { chain -> chain.proceed() }
        hostLoader = loader
    }

    private companion object {
        const val TARGET = "example.host"
    }
}
