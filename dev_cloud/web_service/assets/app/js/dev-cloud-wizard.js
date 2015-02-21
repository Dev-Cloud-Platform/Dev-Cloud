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
        jQuery('#tab2-3').html(content);
        showUsage();
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


window.technology = null

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
        if(getTechnology() != null) {
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


function showUsage() {
    // TODO Need customize.
    // Donut Formatting
    Morris.Donut({
        element: 'chart-CPU',
        data: [
            {value: 70, label: 'used', formatted: 'at least 70%'},
            {value: 30, label: 'free', formatted: 'approx. 30%'}
        ],
        formatter: function (x, data) {
            return data.formatted;
        },
        colors: ['#b92527', '#ffaaab']
    });

    Morris.Donut({
        element: 'chart-RAM',
        data: [
            {value: 70, label: 'foo', formatted: 'at least 70%'},
            {value: 15, label: 'bar', formatted: 'approx. 15%'},
            {value: 10, label: 'baz', formatted: 'approx. 10%'},
            {value: 5, label: 'A really really long label', formatted: 'at most 5%'}
        ],
        formatter: function (x, data) {
            return data.formatted;
        },
        colors: ['#b92527', '#d13c3e', '#ff6264', '#ffaaab']
    });

    Morris.Donut({
        element: 'chart-HDD',
        data: [
            {value: 70, label: 'foo', formatted: 'at least 70%'},
            {value: 15, label: 'bar', formatted: 'approx. 15%'},
            {value: 10, label: 'baz', formatted: 'approx. 10%'},
            {value: 5, label: 'A really really long label', formatted: 'at most 5%'}
        ],
        formatter: function (x, data) {
            return data.formatted;
        },
        colors: ['#b92527', '#d13c3e', '#ff6264', '#ffaaab']
    });
}
