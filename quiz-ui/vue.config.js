const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: process.env.VUE_APP_QUIZ_UI_URL,
  configureWebpack: {
    devServer: {
      headers: { "Access-Control-Allow-Origin": "*",
                 "Access-Control-Allow-Headers": "Content-Type" }
    }
  }
})
