/**
 * viewer.js provides a record viewer for content retrieved from CrossRef or DataCite and
 * ready to be converted in to EPrints XML.
 */

import { Cfg } from "./config.js";

const record_viewer_template = document.createElement('template');

record_viewer_template.innerHTML = `<style>
/* Default CSS */
@import "${Cfg.base_url}/widgets/viewer.css";
/* Site overrides */
@import "/css/site.css";
</style>
<div id="record-viewer" class="record-viewer">
    <div class="viewer-field"><label for="title">Title</label> <div id="title"></div> </div>
    <div class="viewer-field"><label for="alt_title">Alt. Titles</label> <div id="alt_title"></div> </div>
    <div class="viewer-field"><label for="abstract">Abstract</label> <div id="abstract"></div> </div>
    <div class="viewer-field"><label for="creators">Creators</label> <div id="creators"></div> </div>
    <div class="viewer-field"><label for="editors">Editors</label> <div id="editors"></div> </div>
    <div class="viewer-field"><label for="corp_creators">Corp. Creators</label> <div id="corp_creators"></div> </div>
    <div class="viewer-field"><label for="corp_contributors">Corp. Contributors</label> <div id="corp_contributors"></div> </div>
    <div class="viewer-field"><label for="type">Type</label> <div id="type"></div> </div>
    <div class="viewer-field"><label for="doi">DOI</label> <div id="doi"></div> </div>
    <div class="viewer-field"><label for="pmcid">PCMID</label> <div id="pmcid"></div> </div>
    <div class="viewer-field"><label for="pmid">PMID</label> <div id="pmid"></div> </div>
    <div class="viewer-field"><label for="isbn">ISBN</label> <div id="isbn"></div> </div>
    <div class="viewer-field"><label for="issn">ISSN</label> <div id="issn"></div> </div>
    <div class="viewer-field"><label for="related_url">Related URL</label> <div id="related_url"></div> </div>
    <div class="viewer-field"><label for="funders">Funders</label> <div id="funders"></div> </div>
    <div class="viewer-field"><label for="ispublished">Is Published</label> <div id="ispublished"></div> </div>
    <div class="viewer-field"><label for="full_text_status">Full Text Status</label> <div id="full_text_status"></div> </div>
    <div class="viewer-field"><label for="keywords">Keywords</label> <div id="keywords"></div> </div>
    <div class="viewer-field"><label for="subjects">Subjects</label> <div id="subjects"></div> </div>
    <div class="viewer-field"><label for="nonsubj_keywords">Non Subj. Keywords</label> <div id="nonsubj_keywords"></div> </div>
    <div class="viewer-field"><label for="date">Date</label> <div id="date"></div> </div>
    <div class="viewer-field"><label for="date_type">Date Type</label> <div id="date_type"></div> </div>
    <div class="viewer-field"><label for="publication">Publication</label> <div id="publication"></div> </div>
    <div class="viewer-field"><label for="refereed">Refereed</label> <div id="refereed"></div> </div>
    <div class="viewer-field"><label for="series">Series</label> <div id="series"></div> </div>
    <div class="viewer-field"><label for="volume">Volume</label> <div id="volume"></div> </div>
    <div class="viewer-field"><label for="number">No.</label> <div id="number"></div> </div>
    <div class="viewer-field"><label for="publisher">Publisher</label> <div id="publisher"></div> </div>
    <div class="viewer-field"><label for="place_of_pub">Place of Pub.</label> <div id="place_of_pub"></div> </div>
    <div class="viewer-field"><label for="edition">Edition</label> <div id="edition"></div> </div>
    <div class="viewer-field"><label for="pages">Pages</label> <div id="pages"></div> </div>
    <div class="viewer-field"><label for="id_number">ID Number</label> <div id="id_number"></div> </div>
    <div class="viewer-field"><label for="official_url">Official URL</label> <div id="official_url"></div> </div>
    <div class="viewer-field"><label for="alt_url">Alt. URL</label> <div id="alt_url"></div> </div>
    <div class="viewer-field"><label for="official_citation">Official Citation</label> <div id="official_citation"></div> </div>
    <div class="viewer-field"><label for="errata">Errata</label> <div id="errata"></div> </div>
    <div class="viewer-field"><label for="contact_email">Contact EMail</label> <div id="contact_email"></div> </div>
    <div class="viewer-field"><label for="rights">Rights</label> <div id="rights"></div> </div>
    <div class="viewer-field"><label for="copyright_holders">Copyright Holders</label> <div id="copyright_holders"></div> </div>
    <div class="viewer-field"><label for="copyright_statement">Copyright statement</label> <div id="copyright_statement"></div> </div>
    <div class="viewer-field"><label for="note">Note</label> <div id="note"></div> </div>
    <div class="viewer-field"><label for="reviewer">Reviewer</label> <div id="reviewer"></div> </div>
    <div class="viewer-field"><label for="eprint_status">EPrint Status</label> <div id="eprint_status"></div> </div>
    <div class="viewer-field"><label for="collection">Collection</label> <div id="collection"></div> </div>
</div>
`;


/*
 * Utility functions
 */
function yyyymmdd(date) {
    let day = `${date.getDate()}`.padStart(2, '0'),
        month = `${date.getMonth() + 1}`.padStart(2, '0'),
        year = `${date.getFullYear()}`;
    return `${year}-${month}-${day}`
}

function make_person(item, elem) {
    let name_elem = document.createElement('div');
    name_elem.classList.add(`person-name`);
    name_elem.textContent = `${item.name.family}, ${item.name.given}`;
    elem.appendChild(name_elem);
    if ((item.orcid !== undefined) && (item.orcid !== null)) {
        let orcid_elem = document.createElement('a');
        orcid_elem.classList.add('orcid');
        orcid_elem.href = `https://orcid.org/${item.orcid}`;
        orcid_elem.setAttribute('target', '_blank');
        orcid_elem.textContent = item.orcid;
        name_elem.appendChild(orcid_elem);
    }
    elem.appendChild(name_elem);
}

function make_corp(item, elem) {
    let name_elem = document.createElement('div');
    name_elem.classList.add(`corp-name`);
    console.log("DEBUG typeof corp item", typeof(item), item);
    console.log("DEBUG typeof name", typeof(item.name), item.name);
    console.log("DEBUG typeof ror", typeof(item.ror), item.ror);
    name_elem.textContent = item.name;
    elem.appendChild(name_elem);
    if ((item.ror !== undefined) && (item.ror !== null)) {
        let ror_elem = document.createElement('a');
        ror_elem.classList.add('ror');
        ror_elem.href = `https://ror.org/${item.ror}`;
        ror_elem.setAttribute('target', '_blank');
        ror_elem.textContent = item.ror;
        name_elem.appendChild(ror_elem);
    }
    elem.appendChild(name_elem);
}

function make_alt_title(item, elem) {
    let alt_title_elem = document.createElement('div');
    alt_title_elem.classList.add('alt-title');
    alt_title.textContent = item;
    elem.appendChild(alt_title);
}

function make_urls(item, elem) {
    if (item.url !== undefined) {
        let div = document.createElement('div'),
            anchor = document.createElement('a');
        anchor.href = item.url;
        anchor.textContent = item.url;
        anchor.setAttribute('target', '_blank');
        div.classList.add('urls');
        div.appendChild(anchor);
        elem.appendChild(div);
    }
}

function make_funder(item, elem) {
    let div = document.createElement('div');
    div.classList.add('funder');
    if (item.agency !== undefined) {
        let agency = document.createElement('div'),
            label = document.createElement('label'),
            span = document.createElement('span');
        label.setAttribute('for', 'agency');
        label.textContent = 'Agency:';
        span.id = 'agency';
        span.classList.add('funder-agency');
        span.textContent = item.agency;
        agency.classList.add('agency');
        agency.appendChild(label);
        agency.appendChild(span);
        div.appendChild(agency);
    }
    if (item.grant_number !== undefined) {
        let grant = document.createElement('div'),
            label = document.createElement('label'),
            span = document.createElement('span');
        label.setAttribute('for', 'grant_number');
        label.textContent = 'Grant No.: ';
        span.id = 'grant_number';
        span.classList.add('funder-grant_number');
        span.textContent = item.grant_number;
        grant.classList.add('grant-number');
        grant.appendChild(label);
        grant.appendChild(span);
        div.appendChild(grant)
    }
    elem.appendChild(div);
}

function make_subject(item, elem) {
    let div = document.createElement('div');
    div.classList.add('subject');
    div.textContent = item;
    elem.appendChild(div);
}

function make_copyright_holder(item, elem) {
    let div = document.createElement('div');
    div.classList.add('copyright-holder');
    div.textContent = item;
    elem.appendChild(div);
}

function make_nonsubject_keyword(item, elem) {
    let div = document.createElement('div');
    div.classList.add('non-subject-keyword');
    div.textContent = item;
    elem.appendChild(div);
}

/*
 * Webworker friendly classes
 */

/* record_structure describes a simplified outer structure for an "eprint" object useful to Acacia. */
let record_structure = {
    'eprint_status': '',
    'type': '',
    'title': '',
    'alt_title': [],
    'abstract': '',
    'creators': [],
    'editors': [],
    'corp_creators': [],
    'corp_contributors': [],
    'doi': '',
    'pmcid': '',
    'pmid': '',
    'related_url': [],
    'funders': [],
    'ispublished': '',
    'full_text_status': '',
    'keywords': '',
    'subjects': [],
    'nonsubj_keywords': [],
    'date': '',
    'date_type': '',
    'series': '',
    'publication': '',
    'volume': '',
    'number': '',
    'publisher': '',
    'place_of_pub': '',
    'edition': '',
    'pages': 0,
    'refereed': '',
    'isbn': '',
    'issn': '',
    'id_number': '',
    'official_url': '',
    'alt_url': '',
    'official_citation': '',
    'errata': '',
    'contact_email': '',
    'rights': '',
    'copyright_holders': [],
    'copyright_statement': '',
    'note': '',
    'reviewer': '',
    'collection': ''
};


class Record {
    constructor() {
        let self = this;
        self = Object.assign(self, record_structure);
    }

    get value() {
        let obj = {};
        obj = Object.assign(obj, this);
        return obj;
    }

    get as_json() {
        return JSON.stringify(this.value);
    }

    set value(obj) {
        let self = this;
        self = Object.assign(self, obj);
    }
}

/*
 * Viewer classes
 */
class RecordViewer extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({mode: 'open'});
        this.shadowRoot.appendChild(record_viewer_template.content.cloneNode(true));
        this.record = new Record();
    }

    get value() {
        return this.record.value;
    }

    get as_json() {
        return this.record.as_json;
    }

    set value(obj) {
        this.record.value = obj;
        this.refresh_view();    
    }

    refresh_view() {
        let viewer_elem = this.shadowRoot.getElementById('record-viewer'),
            field_names = Object.getOwnPropertyNames(this.record),
            obj = Object.assign({}, this.record);
        for (const key of field_names) {
            let elem = this.shadowRoot.getElementById(key);
            if (elem !== null) {
                switch (key) {
                    case 'creators':
                        if ((obj[key].items !== undefined) && (obj[key].items !== null)) {
                            for (const item of obj[key].items) {
                                make_person(item, elem);
                            }    
                        }
                        break;
                    case 'editors':
                        if ((obj[key].items !== undefined) && (obj[key].items !== null)) {
                            for (const item of obj[key].items) {
                                make_person(item, elem);
                            }    
                        }
                        break;
                    case 'related_url':
                        if ((obj[key].items !== undefined) && (obj[key].items !== null)) {
                            for (const item of obj[key].items) {
                                make_urls(item, elem);
                            }    
                        }
                        break;
                    case 'funders':
                        if ((obj[key].items !== undefined) && (obj[key].items !== null)) {
                            for (const item of obj[key].items) {
                                make_funder(item, elem);
                            }    
                        }
                        break;
                    case 'subjects':
                        if ((obj[key].items !== undefined) && (obj[key].items !== null)) {
                            for (const item of obj[key].items) {
                                make_subject(item, elem);
                            }    
                        }
                        break;
                    case 'corp_creators':
                        if ((obj[key].items !== undefined) && (obj[key].items !== null)) {
                            for (const item of obj[key].items) {
                                make_corp(obj[key].items, elem);
                            }    
                        }
                        break;
                    case 'corp_contributors':
                        if ((obj[key].items !== undefined) && (obj[key].items !== null)) {
                            for (const item of obj[key].items) {
                                make_corp(obj[key].items, elem);
                            }    
                        }
                        break;
                    case 'copyright_holders':
                        if ((obj[key].items !== undefined) && (obj[key].items !== null)) {
                            for (const item of obj[key].items) {
                                make_copyright_holder(obj[key].items, elem);
                            }    
                        }
                        break;
                    case 'alt_title':
                        if ((obj[key].items !== undefined) && (obj[key].items !== null)) {
                            for (const item of obj[key].items) {
                                make_alt_title(obj[key].items, elem);
                            }    
                        }
                        break;
                    case 'nonsubj_keywords':
                        if ((obj[key].items !== undefined) && (obj[key].items !== null)) {
                            for (const item of obj[key].items) {
                                make_nonsubject_keyword(item, elem);
                            }    
                        }
                        break;
                    case 'doi':
                        if (obj[key]) {
                            console.log("DEBUG doi", obj[key]);
                            let anchor = document.createElement('a'),
                                doi = obj[key];
                            anchor.href = `https://doi.org/${doi}`;
                            anchor.setAttribute('target', '_blank');
                            anchor.textContent = doi;
                            console.log("DEBUG anchor", anchor);
                            elem.appendChild(anchor);    
                        }
                        break;
                    default:
                        if (obj.hasOwnProperty(key) && (obj[key] !== null)) {
                            elem.textContent = obj[key];
                        }
                    }    
            } else {
                console.log("DEBUG key does not have an element! ", key)
            }
        }
    }

    connectedCallback() {
        this.refresh_view();
    }

    disconnectedCallback() {
        /* FIXME: Not implemented */
    }

}

export { RecordViewer };
window.customElements.define('record-viewer', RecordViewer);
