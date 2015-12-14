/**
 * Created by m4gik on 14.12.15.
 */

function preCustomize() {
    var application = $(".switch-on :input").val();
    customize(application, 'add');
    styleLoad();
}


function getPublicIP() {
    var ip = ($("#ip .switch-on :input").val() === undefined) ? 'unexpose' : $("#ip .switch-on :input").val();
    setIP(ip);
}


function customize(application, operation) {
    ajaxGet('/main/app/create/environment/customize/' + getTechnology()
        + '/' + application + '/' + operation, function (content) {
        //onSuccess
        setApplications(content);
    });
}


function summary() {
    ajaxGet('/main/app/create/environment/summary/', function (content) {
        //onSuccess
        jQuery('#step4').html(content);
        printInvoiceTemplate(template);
        printInvoicePublicIP();
        printInvoiceDate();
    });
}


function printInvoiceDate() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth(); //January is 0!
    var yyyy = today.getFullYear();
    var months = new Array('January', 'February', 'March', 'April', 'May',
        'June', 'July', 'August', 'September', 'October', 'November', 'December');

    if (dd < 10) {
        dd = '0' + dd;
    }

    today = dd + ' ' + months[mm] + ' ' + yyyy;
    jQuery('#invoice-date').html(today);
}


function printInvoiceTemplate(template) {
    var templateObj = eval('(' + template + ')');
    var information = '<br />CPU: ' + templateObj['cpu'] + ' cores <br />RAM memory: ' + templateObj['memory'] + 'GB';
    jQuery('#template-selected').html(information);
}


function printInvoicePublicIP() {
    if (getIP() == 'expose') {
        jQuery('#public-ip').append('<td class="text-center">3</td> <td>Public IP <span id="public-ip-adresss"></span></td>' +
            ' <td>1</td>  <td class="text-right">$0,00</td>');
    }
}


function defineEnvironment(technology) {
    if (!jQuery('#loadObject').length) {
        jQuery('#step3').prepend('<div id="loadObject" class="row" style="clear:both"><div class="col-md-12" style="margin-left: auto; ' +
            'margin-right: auto; width: 1%;"><img src="/static/app/images/ajax-loader.gif" /></div></div>');
    }
    ajaxGet('/main/app/create/environment/define/' + technology + '/' + getIP(), function (content) {
        //onSuccess
        show_loading_bar({
            pct: 78,
            finish: function (pct) {
                jQuery('#step3').html(content);
                var template = document.getElementById("template").value;
                var requirements = document.getElementById("requirements").value
                setTemplate(template);

                // SelectBoxIt Dropdown replacement
                if ($.isFunction($.fn.selectBoxIt)) {
                    $("select.selectboxit").each(function (i, el) {
                        var $this = $(el),
                            opts = {
                                showFirstOption: attrDefault($this, 'first-option', true),
                                'native': attrDefault($this, 'native', false),
                                defaultText: attrDefault($this, 'text', ''),

                                // Uses the jQuery 'fadeIn' effect when opening the drop down
                                showEffect: "fadeIn",

                                // Sets the jQuery 'fadeIn' effect speed to 400 milleseconds
                                showEffectSpeed: 300,

                                // Uses the jQuery 'fadeOut' effect when closing the drop down
                                hideEffect: "fadeOut",

                                // Sets the jQuery 'fadeOut' effect speed to 400 milleseconds
                                hideEffectSpeed: 300
                            };

                        $this.addClass('visible');
                        $this.selectBoxIt(opts);
                    });

                    var selectBox = $("select.selectboxit");
                    selectBox.data("selectBox-selectBoxIt").selectOption(template);

                    $(function () {
                        // Uses the jQuery bind method to bind to the focus event on the dropdown list
                        $("select.selectboxit").change(function (event, obj) {
                            // Do something when the focus event is triggered
                            updateUsage(requirements, $(this).val())
                            setTemplate($(this).val())
                        });
                    });
                }

                // Popovers and tooltips
                $('[data-toggle="popover"]').each(function (i, el) {
                    var $this = $(el),
                        placement = attrDefault($this, 'placement', 'right'),
                        trigger = attrDefault($this, 'trigger', 'click'),
                        popover_class = $this.hasClass('popover-secondary') ? 'popover-secondary' : ($this.hasClass('popover-primary') ? 'popover-primary' : ($this.hasClass('popover-default') ? 'popover-default' : ''));

                    $this.popover({
                        placement: placement,
                        trigger: trigger,
                        container: "body",
                        html: true
                    });

                    $this.on('shown.bs.popover', function (ev) {
                        var $popover = $this.next();

                        $popover.addClass(popover_class);
                    });
                });

                showUsage(requirements, getTemplate());
                hide_loading_bar();
                jQuery('#loadObject').remove();
            }
        });

    });
}


function styleLoad() {
    $('input.icheck-15').each(function (i, el) {
        var self = $(el),
            label = self.next(),
            label_text = label.text();

        label.remove();

        self.iCheck({
            checkboxClass: 'icheckbox_line-aero',
            radioClass: 'iradio_line-red',
            insert: '<div class="icheck_line-icon"></div>' + label_text
        });
    });
}


window.template = null;
window.applications = null;
window.ip = 'unexpose';

function setTemplate(template) {
    window.template = template;
}

function getTemplate() {
    return window.template;
}

function setApplications(applications) {
    window.applications = applications;
}

function getApplications() {
    return window.applications;
}

function setIP(ip) {
    window.ip = ip;
}

function getIP() {
    return window.ip;
}


function buildAll() {
    var current_application = $(".switch-on :input").val();

    if (current_application != null) {
        preCustomize();
    }

    if (getApplications() != null) {
        defineEnvironment(getTechnology());
        getPublicIP();
    }

    if (getApplications() != null && getTemplate() != null) {
        summary();
    }
}

var cpu = null;
var memory = null;
var space = null;

function showUsage(requirements, template) {
    var requirementsObj = eval('(' + requirements + ')');
    var templateObj = eval('(' + template + ')');

    // Donut Formatting
    cpu = Morris.Donut({
        element: 'chart-CPU',
        data: [
            {
                value: requirementsObj['cpu'],
                label: 'used',
                formatted: requirementsObj['cpu'] + ' cores'
            },
            {
                value: templateObj['cpu'] - requirementsObj['cpu'],
                label: 'free',
                formatted: templateObj['cpu'] - requirementsObj['cpu'] + ' cores'
            }
        ],
        formatter: function (x, data) {
            return data.formatted;
        },
        colors: ['#b92527', '#ffaaab']
    });

    memory = Morris.Donut({
        element: 'chart-RAM',
        data: [
            {
                value: requirementsObj['memory'],
                label: 'used',
                formatted: requirementsObj['memory'] + ' MBs'
            },
            {
                value: (templateObj['memory'] * 1024) - requirementsObj['memory'],
                label: 'free',
                formatted: ((templateObj['memory'] * 1024) - requirementsObj['memory']).toFixed(0) + ' MBs'
            }
        ],
        formatter: function (x, data) {
            return data.formatted;
        },
        colors: ['#242d3c', '#566275']
    });

    space = Morris.Donut({
        element: 'chart-HDD',
        data: [
            {
                value: requirementsObj['space'],
                label: 'used',
                formatted: requirementsObj['space'] + ' MBs'
            },
            {
                value: 10 * 1024 - requirementsObj['space'],
                label: 'free',
                formatted: (10 * 1024 - requirementsObj['space']).toFixed(0) + ' MBs'
            }
        ],
        formatter: function (x, data) {
            return data.formatted;
        },
        colors: ['#D9D022', '#FFF879']
    });
}


function updateUsage(requirements, template) {
    var requirementsObj = eval('(' + requirements + ')');
    var templateObj = eval('(' + template + ')');

    if (cpu != null && memory != null) {
        cpu.setData([
            {
                value: requirementsObj['cpu'],
                label: 'used',
                formatted: requirementsObj['cpu'] + ' cores'
            },
            {
                value: templateObj['cpu'] - requirementsObj['cpu'],
                label: 'free',
                formatted: templateObj['cpu'] - requirementsObj['cpu'] + ' cores'
            }]);

        memory.setData([
            {
                value: requirementsObj['memory'],
                label: 'used',
                formatted: requirementsObj['memory'] + ' MBs'
            },
            {
                value: (templateObj['memory'] * 1024) - requirementsObj['memory'],
                label: 'free',
                formatted: ((templateObj['memory'] * 1024) - requirementsObj['memory']).toFixed(0) + ' MBs'
            }
        ]);

        space.setData([
            {
                value: requirementsObj['space'],
                label: 'used',
                formatted: requirementsObj['space'] + ' MBs'
            },
            {
                value: 10 * 1024 - requirementsObj['space'],
                label: 'free',
                formatted: (10 * 1024 - requirementsObj['space']).toFixed(0) + ' MBs'
            }
        ]);
    }
}

function handler() {
    jQuery('#rootwizard-2').unbind('submit').submit();
}

function showAjaxModal() {
    jQuery("html, body").animate({scrollTop: 0}, "slow");
    jQuery('#modal-7').modal('show', {backdrop: 'static'});

    show_loading_bar({
        pct: 78,
        finish: function (pct) {
            var templateObj = eval('(' + getTemplate() + ')'); //

            ajaxGet('/main/app/create/environment/validation_process/' + templateObj['template_name'] + '/' + getIP(),
                function (content) {
                    //onSuccess
                    jQuery('#modal-7 .modal-body').html(content);

                    ajaxGet('/main/app/create/environment/validation_process_resources/' + templateObj['template_id'],
                        function (content) {
                            //onSuccess
                            jQuery('#modal-7 .modal-body #resources_validation').html(content);

                            if (getIP() == "expose") {
                                ajaxGet('/main/app/create/environment/validation_process_ip_pre/' + getIP(),
                                    function (content) {
                                        //onSuccess
                                        jQuery('#modal-7 .modal-body #ip_validation').html(content);

                                        ajaxGet('/main/app/create/environment/validation_process_ip/' + getIP(),
                                            function (content) {
                                                //onSuccess
                                                jQuery('#modal-7 .modal-body #ip_validation').html(content);
                                                if (jQuery('#resource_validation i').hasClass('entypo-check')
                                                    && jQuery('#ip_validation i').hasClass('entypo-check')) {
                                                    jQuery('.modal-footer').append('<button type="button" id="start" class="btn btn-info">Launch VM</button>');
                                                    jQuery('#start').each(function () {
                                                        jQuery(this).click(handler);
                                                    });
                                                }
                                            });
                                    });
                            } else {
                                if (jQuery('#resource_validation i').hasClass('entypo-check')) {
                                    jQuery('.modal-footer').append('<button type="button" id="start" class="btn btn-info">Launch VM</button>');
                                    jQuery('#start').each(function () {
                                        jQuery(this).click(handler);
                                    });
                                }
                            }
                        });
                });

            hide_loading_bar();
        }
    });
}


jQuery(document).ready(function () {
    jQuery('#rootwizard-2').submit(function (e) {
        if (jQuery('div.checkbox').hasClass('checked')) {
            e.preventDefault();
            showAjaxModal();
        }
    });
});

