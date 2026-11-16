/* Read-only geometry checks against the report actually rendered by Desktop.
 * Start Desktop with local WebView debugging, refresh the report, then run:
 * PLAYWRIGHT_MODULE=<module path> node scripts/check_powerbi_layout.cjs
 */
const path = require('node:path');
const fs = require('node:fs/promises');
const crypto = require('node:crypto');
const ROOT = process.env.DSS_REPO_ROOT || path.resolve(__dirname, '..');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || path.join(ROOT, '.cache/browser/node_modules/playwright'));
const definitions = path.join(ROOT, 'dashboards/powerbi/Delivery.Report/definition/pages');
const output = path.join(ROOT, '.cache/dashboard-native');
const id = key => crypto.createHash('sha256').update(key).digest('hex').slice(0,20);
const pages = [['Tổng quan','overview','62.897'], ['Rủi ro','risk','89,0%'], ['Cam kết','promises','26,8%'],
               ['Tuyến giao','routing','1.823.661'], ['Lịch trình tuyến','routing_detail','1.823.661']];

async function manifest(key) {
  const folder = path.join(definitions, id(key), 'visuals');
  const items = {};
  for (const name of await fs.readdir(folder)) {
    const data = JSON.parse(await fs.readFile(path.join(folder, name, 'visual.json'), 'utf8'));
    items[data.name] = {kind: data.visual.visualType, background: data.annotations?.some(a => a.name==='designRole' && a.value==='background'), hidden:data.isHidden};
  }
  return items;
}

(async()=>{
  const browser = await chromium.connectOverCDP(process.env.POWERBI_CDP_URL || 'http://127.0.0.1:9223');
  try {
    const page = browser.contexts().flatMap(c=>c.pages()).find(p=>p.url().includes('reportView'));
    if(!page)throw Error('Open and refresh the target report in Power BI Desktop first.');
    await page.bringToFront();
    const canvas = page.locator('[data-testid="display-area"]');
    await page.keyboard.press('Escape');
    await canvas.getByRole('button',{name:'Tổng quan',exact:true}).click({modifiers:['Control'],force:true});
    await canvas.getByText('62.897',{exact:true}).waitFor({timeout:40000});
    const pending=page.getByRole('button',{name:'Apply changes',exact:true});
    if(await pending.count()){await pending.first().click({force:true});await pending.first().waitFor({state:'hidden',timeout:40000});}
    const dismiss=page.locator('[data-testid="tri-message-bar-dismiss-button"]');
    while(await dismiss.count())await dismiss.first().click({force:true});
    await fs.mkdir(output,{recursive:true});
    const client=await page.context().newCDPSession(page);
    await client.send('Emulation.setFocusEmulationEnabled',{enabled:true});
    const records=[];
    for(const viewport of [{width:2400,height:1580},{width:1366,height:900}]) {
      await client.send('Emulation.setDeviceMetricsOverride',{...viewport,deviceScaleFactor:1,mobile:false});
      for(const [label,key,value]of pages) {
        if(key==='routing_detail')await canvas.getByText('Xem lịch trình chi tiết',{exact:true}).click({modifiers:['Control'],force:true});
        else await canvas.getByRole('button',{name:label,exact:true}).click({modifiers:['Control'],force:true});
        await canvas.getByText(value,{exact:true}).waitFor({timeout:40000});
        await page.waitForTimeout(2500);
        let previous='',stable=0;
        for(let attempt=0;attempt<24 && stable<3;attempt++) {
          const signature=await canvas.evaluate(root=>JSON.stringify([...root.querySelectorAll('svg text,[role="columnheader"],[role="gridcell"][column-index]')].map(e=>{const r=e.getBoundingClientRect();return [e.textContent,Math.round(r.x*2),Math.round(r.y*2),Math.round(r.width*2),Math.round(r.height*2)]})));
          stable=signature===previous?stable+1:0;previous=signature;
          await page.waitForTimeout(250);
        }
        const box=await canvas.boundingBox();
        // Click an actual empty canvas margin to clear Desktop selection borders.
        await canvas.click({position:{x:box.width-4,y:box.height-4},force:true});
        await page.mouse.move(5,5);
        const check=await canvas.evaluate((root,items)=>{
          const rect=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}};
          const overlap=(a,b)=>Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>1.5 && Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>1.5;
          const issues=[],foreground=[],words=[],tables=[];
          let chartLabelsChecked=0,tableCellsChecked=0,axisLabelsChecked=0;
          for(const group of root.querySelectorAll('.visualContainer')) {
            const label=group.querySelector('[id^="visualsLabel-"]');
            if(!label)continue;
            const name=label.id.slice('visualsLabel-'.length), source=items[name];
            if(!source || source.hidden)continue;
            const bounds=rect(group);
            if(bounds.w<1 || bounds.h<1)continue;
            if(!source.background)foreground.push({name,kind:source.kind,...bounds});
            if(['textbox','card','slicer'].includes(source.kind) && !source.background) {
              const walker=document.createTreeWalker(group,NodeFilter.SHOW_TEXT);
              for(let node=walker.nextNode();node;node=walker.nextNode()) {
                if(!node.textContent.trim())continue;
                const parent=node.parentElement;
                if(!parent || parent.closest('[aria-hidden="true"],[role="tooltip"],title,desc,button.visualHeaderItemContainer'))continue;
                if(getComputedStyle(parent).visibility==='hidden')continue;
                const range=document.createRange();range.selectNodeContents(node);
                for(const r of range.getClientRects()) {
                  if(r.width<1 || r.height<1)continue;
                  const w={name,text:node.textContent.trim(),x:r.x,y:r.y,w:r.width,h:r.height};
                  if(w.x<bounds.x-2 || w.y<bounds.y-2 || w.x+w.w>bounds.x+bounds.w+2 || w.y+w.h>bounds.y+bounds.h+2)
                    issues.push({type:'text_outside_own_visual',kind:source.kind,...w,bounds});
                  words.push(w);
                }
              }
            }
            if(source.kind==='tableEx') {
              const columns=[...group.querySelectorAll('[role="columnheader"]')].filter(e=>e.getAttribute('data-query-ref'));
              if(columns.length) {
                const cells=columns.map(rect), min=Math.min(...cells.map(c=>c.x)),max=Math.max(...cells.map(c=>c.x+c.w));
                const coverage=(max-min)/bounds.w;
                tables.push({columns:columns.length,coverage:Number(coverage.toFixed(3))});
                if(coverage<0.88 || coverage>1.01)issues.push({type:'table_width_not_filled',coverage});
                for(const column of columns) {
                  if(column.scrollWidth>column.clientWidth+2)issues.push({type:'truncated_table_header',text:column.innerText});
                }
                const headers=new Map(columns.map(e=>[e.getAttribute('column-index'),rect(e)]));
                for(const cell of group.querySelectorAll('[role="gridcell"][column-index][data-query-ref]')) {
                  const header=headers.get(cell.getAttribute('column-index'));
                  if(!header)continue;
                  const bounds=rect(cell);tableCellsChecked++;
                  if(Math.abs(bounds.x-header.x)>2 || Math.abs(bounds.w-header.w)>2)issues.push({type:'table_cell_not_aligned_with_header',text:cell.innerText,bounds,header});
                }
              }
            }
            if(['clusteredBarChart','barChart'].includes(source.kind)) {
              const labels=[...group.querySelectorAll('text.label')]
                .filter(e=>getComputedStyle(e).visibility!=='hidden').map(e=>({text:e.textContent,...rect(e)})).filter(r=>r.w>1&&r.h>1);
              chartLabelsChecked+=labels.length;
              for(let i=0;i<labels.length;i++)for(let j=i+1;j<labels.length;j++)if(overlap(labels[i],labels[j]))issues.push({type:'chart_label_overlap',a:labels[i],b:labels[j]});
              for(const axis of group.querySelectorAll('g.x.axis,g.y.axis')) {
                const ticks=[...axis.querySelectorAll('g.tick text')].map(e=>({text:e.textContent,...rect(e)})).filter(r=>r.w>1&&r.h>1);
                axisLabelsChecked+=ticks.length;
                for(let i=0;i<ticks.length;i++)for(let j=i+1;j<ticks.length;j++)if(overlap(ticks[i],ticks[j]))issues.push({type:'axis_label_overlap',a:ticks[i],b:ticks[j]});
              }
            }
          }
          for(let i=0;i<foreground.length;i++)for(let j=i+1;j<foreground.length;j++)if(overlap(foreground[i],foreground[j]))issues.push({type:'foreground_visual_overlap',a:foreground[i].name,b:foreground[j].name});
          for(let i=0;i<words.length;i++)for(let j=i+1;j<words.length;j++)if(words[i].name!==words[j].name && overlap(words[i],words[j]))issues.push({type:'foreground_text_overlap',a:words[i],b:words[j]});
          if(!tableCellsChecked)issues.push({type:'no_table_cells_measured'});
          if(!chartLabelsChecked && Object.values(items).some(v=>['clusteredBarChart','barChart'].includes(v.kind)))issues.push({type:'no_chart_labels_measured'});
          return {foreground_visuals_checked:foreground.length,text_rectangles_checked:words.length,chart_labels_checked:chartLabelsChecked,axis_labels_checked:axisLabelsChecked,table_cells_checked:tableCellsChecked,tables,issues};
        },await manifest(key));
        if(key==='promises' && check.chart_labels_checked!==8)check.issues.push({type:'paired_chart_missing_labels',expected:8,actual:check.chart_labels_checked});
        const text=await canvas.innerText();
        if(/See details|Something went wrong|Couldn't load|Phụ trách|Anh Quốc/.test(text))check.issues.push({type:'unexpected_report_content'});
        records.push({page:key,viewport,...check});
        await canvas.screenshot({path:path.join(output,`${key}_${viewport.width}.png`)});
        console.log(`${check.issues.length?'FAIL':'PASS'} ${key} ${viewport.width}: ${check.foreground_visuals_checked} visual regions, ${check.text_rectangles_checked} text rectangles, ${check.issues.length} issues`);
      }
    }
    await canvas.getByRole('button',{name:'Tổng quan',exact:true}).click({modifiers:['Control'],force:true});
    const result={all_passed:records.every(r=>!r.issues.length),scope:'Actual native Power BI WebView geometry, not HTML preview or only source rectangles',limitations:'Checks visible default states at two render sizes. Route stop tables intentionally scroll; chart interpretation and intentional map layers still require visual review.',records};
    await fs.writeFile(path.join(ROOT,'reports/dashboard/native_layout_validation.json'),JSON.stringify(result,null,2)+'\n');
    if(!result.all_passed)throw Error('Native layout issues found. See native_layout_validation.json.');
  }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
