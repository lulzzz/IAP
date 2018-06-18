/*
Function to control the worldmap
*/
$(document).ready(function () {

    // Variable definition
    var current_page_container = $('#content .container_reference.is_loaded.active');

    var this_div = current_page_container.find('.worldmap.load-js-controller').first();
    this_div.removeClass('load-js-controller');
    var url_action = this_div.parent().parent().parent().attr('url_action');

    if (typeof($.fn.vectorMap) === 'undefined') {
        return;
    }

    if (this_div.length) {

        // Perform JSON request to load data into table
        $.getJSON(url_action, function(data) {

            this_div.vectorMap({
                map: 'world_en',
                backgroundColor: null,
                color: '#ffffff',
                hoverOpacity: 0.7,
                selectedColor: '#999999',
                enableZoom: true,
                showTooltip: true,
                values: data,
                scaleColors: ['#f1b585', '#EF8E3F'],
                normalizeFunction: 'polynomial',
                onLabelShow: function (event, label, code) {
                    var count = 0;
                    if (data[code] != null) {
                        if (!isNaN(data[code])) {
                            count = parseInt(data[code]).toLocaleString();

                            var count_text = 'occurrence';
                            if (count > 1) {
                                count_text = 'occurrences';
                            }
                            label.html(label.html()+' ('+ count + ' ' + count_text + ')');
                        }
                    }
                }
            });

        });

    }

});
