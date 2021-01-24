module.exports = {
    runtimeCompiler: true,
    devServer: {
        // https: true,
    },
    pwa: {
        workboxPluginMode: "InjectManifest",
        workboxOptions: {
            swSrc: "src/service-worker.js",
            exclude: [/\.map$/, /manifest\.json$/],
        },
    },
};
