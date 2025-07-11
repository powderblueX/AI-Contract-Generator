# 部委合同抓取
## 1. 安装google浏览器插件web scraper
## 2. F12检查->选择web scraper->create new sitemap->import sitemap
以下复制粘贴即可导入抓取脚本
{"_id":"buweiTest","startUrl":["https://htsfwb.samr.gov.cn/National"],"selectors":[{"id":"enter","parentSelectors":["container"],"type":"SelectorLink","selector":".item-box a","multiple":true,"linkType":"linkFromHref"},{"id":"download","parentSelectors":["enter"],"type":"SelectorElementClick","clickActionType":"real","clickElementSelector":"button.download-word","clickElementUniquenessType":"uniqueText","clickType":"clickOnce","delay":3000,"discardInitialElements":"do-not-discard","multiple":false,"selector":"button.download-word"},{"id":"container","parentSelectors":["_root"],"type":"SelectorElementClick","clickActionType":"real","clickElementSelector":"a:nth-of-type(n+2)","clickElementUniquenessType":"uniqueText","clickType":"clickOnce","delay":2000,"discardInitialElements":"do-not-discard","multiple":true,"selector":"div.samr-pl-4"}]}
## 3. 点击新建的sitemap->点击sitemap xxx（你取的名字）->点击Scrape

*** 
# 地方合同抓取
## 1. 同上
## 2. F12检查->选择web scraper->create new sitemap->import sitemap
以下复制粘贴即可导入抓取脚本
{"_id":"difang","startUrl":["https://htsfwb.samr.gov.cn/Local"],"selectors":[{"id":"enter","parentSelectors":["container"],"type":"SelectorLink","selector":".item-box a","multiple":true,"linkType":"linkFromHref"},{"id":"download","parentSelectors":["enter"],"type":"SelectorElementClick","clickActionType":"real","clickElementSelector":"button.download-word","clickElementUniquenessType":"uniqueText","clickType":"clickOnce","delay":2000,"discardInitialElements":"do-not-discard","multiple":false,"selector":"button.download-word"},{"id":"container","parentSelectors":["_root"],"type":"SelectorElementClick","clickActionType":"real","clickElementSelector":"a:nth-of-type(n+2)","clickElementUniquenessType":"uniqueText","clickType":"clickOnce","delay":2000,"discardInitialElements":"do-not-discard","multiple":true,"selector":"div.samr-pl-4"}]}
## 3. 点击新建的sitemap->点击sitemap xxx（你取的名字）->点击Scrape
