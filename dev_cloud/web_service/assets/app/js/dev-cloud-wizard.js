/**
 * Created by m4gik on 21.02.15.
 */

function generateDependencies() {
    var technology = $(".switch-on :input").val()
    setTechnology(technology)
    ajaxGet('/main/app/create/environment/technology/' + getTechnology(), function (content) {
        //onSuccess
        jQuery('#tab2-2').html(content);
        styleLoad();
    })
}


function customize(application, operation) {
    ajaxGet('/main/app/create/environment/customize/' + getTechnology()
    + '/' + application + '/' + operation, function (content) {
        //onSuccess
    })
}


function defineEnvironment(technology) {
    ajaxGet('/main/app/create/environment/define/' + technology, function (content) {
        //onSuccess
        jQuery('#step3').html(content);
        var template = document.getElementById("template").value;
        var requirements = document.getElementById("requirements").value

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
                });
            });
        }

        showUsage(requirements, template);
    })
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

    $(function () {

        var $draggable_portlets = $(".draggable-portlets");

        $(".draggable-portlets .sorted").sortable({
            connectWith: ".draggable-portlets .sorted",
            handle: '.panel-heading',
            start: function (event, ui) {
                $draggable_portlets.addClass('dragging');
            },
            stop: function () {
                $draggable_portlets.removeClass('dragging');
            },
            receive: function (event, ui) {
                if (this.id == 'selected_apps') {
                    customize(ui.item.find('h4').text(), 'add')
                } else {
                    customize(ui.item.find('h4').text(), 'remove')
                }
            }
        });

        $(".draggable-portlets .sorted .panel-heading").disableSelection();
    });
}


window.technology = null;

function setTechnology(technology) {
    window.technology = technology
}

function getTechnology() {
    return window.technology
}


function buildAll() {
    var current_technology = $(".switch-on :input").val();
    if (current_technology != getTechnology() && getTechnology() != null) {
        show_loading_bar({
            pct: 78,
            finish: function (pct) {
                generateDependencies();
                hide_loading_bar();
            }
        });

    } else if (getTechnology() == null) {
        setTechnology(current_technology);
        if (getTechnology() != null) {
            show_loading_bar({
                pct: 78,
                finish: function (pct) {
                    generateDependencies();
                    hide_loading_bar();
                }
            });
        }
    }

    defineEnvironment(getTechnology());
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
