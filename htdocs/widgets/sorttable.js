/**
 * sorttable.js provides a sortable table support. This code is based on
 * the example at Mozilla Developer Network website on working with
 * table elements.
 *
 * See: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/table
 *
 */
"use strict";

function make_table_sortable(css_selector = 'table') {
  let sort_ascending = true;
  for (let table of document.querySelectorAll(css_selector)) {
    for (let th of table.tHead.rows[0].cells) {
      th.onclick = function() {
        const tBody = table.tBodies[0];
        const rows = tBody.rows;
        for (let tr of rows) {
          Array.prototype.slice.call(rows)
            .sort(function(tr1, tr2){
              const cellIndex = th.cellIndex;
              if (sort_ascending) {
                return tr1.cells[cellIndex].textContent.localeCompare(tr2.cells[cellIndex].textContent);
              } else {
                return tr2.cells[cellIndex].textContent.localeCompare(tr1.cells[cellIndex].textContent);
              }
            })
            .forEach(function(tr){
              this.appendChild(this.removeChild(tr));
            }, tBody);
        }
        if (sort_ascending) {
            sort_ascending = false;
        } else {
            sort_ascending = true;
        }
      }
    }
  }
}

export { make_table_sortable };

