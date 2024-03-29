class BulmaModal {
    constructor(selector) {
        this.elem = document.querySelector(selector)
        this.close_data()
    }
    
    show() {
        this.elem.classList.toggle('is-active')
        this.on_show()
    }
    
    close() {
        this.elem.classList.toggle('is-active')
        this.on_close()
    }
    
    close_data() {
        var modalClose = this.elem.querySelectorAll("[data-bulma-modal='close'], .modal-background")
        var that = this
        modalClose.forEach(function(e) {
            e.addEventListener("click", function() {
                
                that.elem.classList.toggle('is-active')

                var event = new Event('modal:close')

                that.elem.dispatchEvent(event);
            })
        })
    }
    
    on_show() {
        var event = new Event('modal:show')
    
        this.elem.dispatchEvent(event);
    }
    
    on_close() {
        var event = new Event('modal:close')
    
        this.elem.dispatchEvent(event);
    }
    
    addEventListener(event, callback) {
        this.elem.addEventListener(event, callback)
    }
}

var btn1 = document.querySelector("#btn1")
var btn2 = document.querySelector("#btn2")
var mdl = new BulmaModal("#myModal")

if (btn1 != null){
    btn1.addEventListener("click", function () {
        mdl.show()
    })
}

if (btn2 != null){
    btn2.addEventListener("click", function () {
        mdl.show()
    })
}

var input = document.getElementById("valueToGo");
input.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        document.getElementById("btnToGo").click();
    }
});