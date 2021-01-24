module.exports = {
    runtimeCompiler: true,
    devServer: {
        // https: true,
    },
    pwa: {
        workboxOptions: {
            importScripts: ["src/service-worker.ts"],
        },
    },
};
