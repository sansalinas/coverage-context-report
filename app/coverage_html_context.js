

coverage_show_line_context = function () {

    var files = @@files@@;
    var contexts = @@contexts@@;
    var arcs = @@arcs@@;

    function get_current_file_id(){
        var pagePathName= window.location.pathname;
        current_file = pagePathName.substring(pagePathName.lastIndexOf("/") + 1);
        current_file = current_file.substring(0,current_file.indexOf(".html"));
        var files_filter = files.filter(file => file.path.replace(/[&\/\\#,+()$~%.'":*?<>{}]/g,'_').endsWith(current_file));
        if (files_filter.length){
            console.log('Coverage context report for file ', files_filter[0]);
            return files_filter[0].id
        }
        return null
    }

    function show_file_comment(arc_file){
        arc_file['context'].forEach(context => show_context_comment(context));
    }

    function show_context_comment(arc_context){
        context = contexts.filter(context => context.id == arc_context['id'])[0]['context'];
        if (context){
            arc_context['arcs'].forEach(arc => show_arc_comment(context, arc));
        }
    }

    function show_arc_comment(context, arc){
        if(arc > 0){
            var line = $("p#t" + arc);
            if(line.length){
                line.addClass("show_par");
                span_r = line.find("span.r");
                if(span_r.length){
                    line_context = span_r.find("span.annotate.long");
                    if(line_context.length == 0){
                        span_r.prepend('<span class="annotate long"></span>');
                    }
                    line_context = span_r.find("span.annotate.long")[0];
                    if(line_context.innerHTML.indexOf(context) == -1) {
                        line_context.append(context + '\r\n');
                    }
                }
            }
        }
    }

    file_id = get_current_file_id();
    if(file_id){
        arcs_file = arcs.filter(arc => arc.id == file_id);
        arcs_file.forEach(arc_file => show_file_comment(arc_file));
    } else{
        console.log('file not found, continue without show line context');
    }
};

jQuery(document).ready(coverage_show_line_context);