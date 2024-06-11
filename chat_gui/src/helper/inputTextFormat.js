export function textToHtml(strData) {
  // 用一个不存在的样式来替换换行 保证来回的切换
  return strData.replace(/\n/g, '<br class="__NEW__LINE__"/>');
}

export function htmlToText(strData) {
  return strData.replace(/<br class="__NEW__LINE__"\/>/g, "\n");
}
