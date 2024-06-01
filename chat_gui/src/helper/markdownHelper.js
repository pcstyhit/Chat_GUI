// 引入依赖
import MarkdownIt from "markdown-it";
import hljs from "highlight.js/lib/core";

// 引入需要的相关语言包
import accesslog from "highlight.js/lib/languages/accesslog";
import bash from "highlight.js/lib/languages/bash";
import dockerfile from "highlight.js/lib/languages/dockerfile";
import javascript from "highlight.js/lib/languages/javascript";
import handlebars from "highlight.js/lib/languages/handlebars";
import java from "highlight.js/lib/languages/java";
import json from "highlight.js/lib/languages/json";
import nginx from "highlight.js/lib/languages/nginx";
import shell from "highlight.js/lib/languages/shell";
import sql from "highlight.js/lib/languages/sql";
import typescript from "highlight.js/lib/languages/typescript";
import xml from "highlight.js/lib/languages/xml";
import yaml from "highlight.js/lib/languages/yaml";

import * as SVGS from '../assets/styles/chat/svgs'

// 语言包需要注册
hljs.registerLanguage("accesslog", accesslog);
hljs.registerLanguage("bash", bash);
hljs.registerLanguage("dockerfile", dockerfile);
hljs.registerLanguage("javascript", javascript);
hljs.registerLanguage("json", json);
hljs.registerLanguage("nginx", nginx);
hljs.registerLanguage("handlebars", handlebars);
hljs.registerLanguage("typescript", typescript);
hljs.registerLanguage("java", java);
hljs.registerLanguage("yaml", yaml);
hljs.registerLanguage("sql", sql);
hljs.registerLanguage("shell", shell);
hljs.registerLanguage("xml", xml);

const marked = new MarkdownIt({
  highlight: function (str, lang) {
    console.log("get language: ", lang, hljs.getLanguage(lang));
    if (lang && hljs.getLanguage(lang)) {

      try {
        return (`
          <div class="text code-block">
            <div class="copy-header">
              <el-text class="lang">${lang}</el-text>
              <button class="copy-button" onclick="copyToClipboard(this)">${SVGS.copyCodeIcon}</button>
              <el-text class="copy-text">Copy code</el-text>
            </div> 
            <pre class="hljs"><code>${hljs.highlight(str, { language: lang }).value}</code></pre>
          </div> 
          `
        );
      } catch (__) {
        //
      }
    }
    return "";
  },
});

marked.use(md=>{
  const defaultRender = md.renderer.rules.fence || function(tokens,idx,options,env,self){
    return self.renderToken(tokens,idx,options);
  };

  md.renderer.rules.fence = (tokens,idx,options,env,self)=>{
    const token = tokens[idx];
    const info = token.info ? md.utils.unescapeAll(token.info).trim() : '';
    const langName = info.split(/\s+/g)[0];


    console.log(langName)

    return `
      <div class="text code-rendered">
        ${defaultRender(tokens,idx,options,env,self)}
      </div> 
      `;
  }
})

export default marked;
