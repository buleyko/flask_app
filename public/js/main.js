const csrftoken = document.querySelector('meta[name="csrf-token"]').content
const fetchHeaders = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken,
}
class Logger {
    constructor(options) {
        this.infoMsgPrefix = options.infPref;
        this.errorMsgPrefix = options.errPref;
        this.off = options.off;
    }
    info(msg='') {
        if (!this.off) {
            console.log(`${this.infoMsgPrefix}: ${this.name}: ${msg}`);
        }
    }
    error(msg='') {
        if (!this.off) {
            console.log(`${this.errorMsgPrefix}: ${this.name}: ${msg}`);
        }
    }
}

const logger = new Logger({
    infPref: 'INFO',
    errPref: 'ERROR',
    off: false,
})

class LocalStorageManager {
    set(key, value) {
        localStorage.setItem(key, value);
    }
    get(key) {
        return localStorage.getItem(key);
    }
    delete(key) {
        localStorage.removeItem(key);
    }
    clear() {
        localStorage.clear();
    }
}
const storage = new LocalStorageManager()


const isExist = (obj) => {
    return (obj != null && obj !== undefined || (Array.isArray(obj) && obj.length != 0))
}

const parseIntOrZero = (val) => {
    const parsed = parseInt(val);
    return (isNaN(parsed))? 0 : parsed; 
}

const inputDefault = (defVal) => {
    return function() {
        event.target.value = (event.target.value.length == 0)? defVal : event.target.value;
    };
};
const inputDefaultOne = inputDefault(1);

const onlyOneToNine = (evt) => {
    var ASCIICode = (evt.which) ? evt.which : evt.keyCode
    if (ASCIICode > 31 && (ASCIICode < 49 || ASCIICode > 57)) {
        return false;
    }
    return true;
} // <input type="text" onkeypress="return onlyOneToNine(event);">

const onlyZeroToNine = (evt) => {
    var ASCIICode = (evt.which) ? evt.which : evt.keyCode
    if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57)) {
        return false;
    }
    return true;
} // <input type="text" onkeypress="return onlyZeroToNine(event);">

const getBySelector = (selector, single=true) => {
    let res = null;
    if (single) {
        try {
            res = document.querySelector(selector);
        } catch(e) {
            if (e instanceof SyntaxError) {
                logger.info.call(this, `selector syntax ${selector}`);
            } else {
                logger.info.call(this, `querySelector by:${selector}`);
            }
        }
        if (res == null) {
            logger.info.call(this, `element(s) with selector ${selector} undefined`); 
        }
        return res;
    } else {
        try {
            res = document.querySelectorAll(selector);
        } catch(e) {
            if (e instanceof SyntaxError) {
                logger.info.call(this, `selector syntax ${selector}`);
            } else {
                logger.info.call(this, `querySelectorAll by:${selector}`);
            }
        }
        if (res.length == 0) {
            logger.info.call(this, `element(s) with selector ${selector} undefined`);
            return [];
        }
        return [...res];
    }
}

const getInnerHtml = (selector) => {
    let res = getBySelector(selector);
    if (isExist(res)) { 
        return res.innerHTML;
    }
}
const setInnerHtml = (selector, innerData) => {
    let res = getBySelector(selector);
    if (isExist(res)) { 
        res.innerHTML = innerData;
    }
}

Array.prototype.findElementIndex = function(el) {
    const index = this.indexOf(el);
    return (index != -1) ? index : null;
}

Element.prototype.hiddenParentByСondition = function(condition) {
    if (condition) {
        if (this.parentElement.classList.contains('hidden')) {
            this.parentElement.classList.remove('hidden');
        }
    } else {
        if (!this.parentElement.classList.contains('hidden')) {
            this.parentElement.classList.add('hidden');
        }
    }
}

class FetchDataException extends Error {
    constructor(message, options=null) {
        super(message, options);
    }
}

async function fetchAsync(method, url, data) {

    const requestOptions = {
        method: method,
        headers: fetchHeaders,
        body: JSON.stringify(data)
    };
    try {
        const response = await fetch(url, requestOptions);
        const res = await response.json();
        return res;
    } catch (e) {
        throw new FetchDataException(`ERROR: fetch data by URL: ${url}: ${e}`);
    }
}


class CssClassManager {
    
    add(selector, className, single=true) {
        let res = getBySelector(selector, single);
        if (isExist(res)) { 
            if (Array.isArray(res)) {
                res.forEach(el => {
                    if(!el.classList.contains(className)) {
                        el.classList.add(className)
                    }
                })
            } else {
                if(!res.classList.contains(className)) {
                    res.classList.add(className)
                }
            }
        }
    }
    remove(selector, className, single=true) {
        let res = getBySelector(selector, single);
        if (isExist(res)) { 
            if (Array.isArray(res)) {
                res.forEach(el => {
                    if(el.classList.contains(className)) {
                        el.classList.remove(className)
                    }
                })
            } else {
                if(res.classList.contains(className)) {
                    res.classList.remove(className)
                }
            }
        }
    }
    toggle(selector, className, single=true) {
        let res = getBySelector(selector, single);
        if (isExist(res)) { 
            if (Array.isArray(res)) {
                res.forEach(el => {
                    el.classList.toggle(className)
                })
            } else {
                res.classList.toggle(className)
            }
        }
    }
    changeOrAddAt(selector, from, to, single=true) {
        let res = getBySelector(selector, single);
        if (isExist(res)) { 
            if (Array.isArray(res)) {
                res.forEach(el => {
                    if(!el.classList.contains(from)) {
                        el.classList.add(from)
                    } else {
                        el.classList.toggle(from)
                        el.classList.toggle(to)
                    }
                })
            } else {
                if(!res.classList.contains(from)) {
                    res.classList.add(from)
                } else {
                    res.classList.toggle(from)
                    res.classList.toggle(to)
                }
            }
        }
        
    }
    changeByPref(classes, single=true) {
        /* Change each class that start with prefix(until '-'), remove old valua and add new */
        classes.split(' ').forEach(className => {
            const namePref = className.split('-')[0];
            let res = getBySelector(`[class*="${namePref}"]`, single);
            if (isExist(res)) { 
                if (Array.isArray(res)) {
                    res.forEach(el => {
                        el.classList.forEach(name => {
                            if(name.startsWith(namePref) && name != className) { 
                                el.classList.toggle(name)
                                el.classList.toggle(className)
                            }
                        })
                    })
                } else {
                    res.classList.forEach(name => {
                        if(name.startsWith(namePref) && name != className) {
                            res.classList.toggle(name)
                            res.classList.toggle(className)
                        }
                    })
                }
            }
            
        })
    }
}

const cssClass = new CssClassManager()

const setOptions = (optionObj) => {
    const data = optionObj;
    fetch('/options/', {  
        method: 'post',  
        headers: fetchHeaders,
        body: JSON.stringify(data)
    })
    .then((response) => {
        return response.json()
    })  
    .then((json) => {
        console.log('Request succeeded with JSON response', json);  
    })  
    .catch(function (error) {  
        console.log('Request failed', error);  
    });
}
theme.serverHandler = setOptions

class Observable {
    constructor() {
        this.observers = [];
    }
    subscribe(func) {
        this.observers.push(func);
    }
    unsubscribe(func) {
        this.observers = this.observers.filter(subscriber => subscriber !== func);
    }
    signal(data) {
        this.observers.forEach(observer => observer(data));
    }
}

class ElementWatcher {
    constructor(options) {
        this.obserEvent = options.obserEvent;
        this.obserElements = document.querySelectorAll(options.obserElementsSelector);
        this.eventler = options.eventler;
        this.handler = options.handler;
        this.setup();
    }
    setup() {
        this.obserElements.forEach((el) => {
            el.addEventListener(this.obserEvent, this.checkEvent);
        });
    }
    checkEvent = () => {
        this.eventler();
        this.handler();
    }   
}



