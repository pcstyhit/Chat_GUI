const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: '127.0.0.1',
    port: 10090,
  },
  outputDir: '../chat_gui_server/statics',
},)
