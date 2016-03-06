$(function() {
    
    // ADD/REMOVE HISTORY
    $('.add-remove-history').click(function(e) {
        e.preventDefault();
        var link = this;
        var content = $(link).html();
        $(link).html('<i class="fa fa-spinner fa-spin"></i>');
        var movie_id = $(this).data('movieId');
        var url = "/ajax/history_add_remove";
        var csrftoken = getCookie('csrftoken');
        var post_data = {
            'movie_id': movie_id,
            'csrfmiddlewaretoken': csrftoken,
        };
        $.post(url, post_data, function(data) {
            if (data == "added") {
                $(link).addClass('history-active');
                // remove from watchlist and blocklist
                $('#movie-'+movie_id+' .add-remove-watchlist').removeClass('watchlist-active');
                $('#movie-'+movie_id+' .add-remove-blocklist').removeClass('blocklist-active');
            } else if (data == "removed") {
                $(link).removeClass('history-active');
            }
            $(link).html(content);
        }).fail(function() {
            $(link).html('<i class="fa fa-exclamation-triangle"></i>');
        }).always(function() {
            $(link).blur();
            $(link).tooltip('hide');
        });
        return false;
    });
    
    // ADD/REMOVE WATCHLIST
    $('.add-remove-watchlist').click(function(e) {
        e.preventDefault();
        var link = this;
        var content = $(link).html();
        $(link).html('<i class="fa fa-spinner fa-spin"></i>');
        var movie_id = $(this).data('movieId');
        var url = "/ajax/watchlist_add_remove";
        var csrftoken = getCookie('csrftoken');
        var post_data = {
            'movie_id': movie_id,
            'csrfmiddlewaretoken': csrftoken,
        };
        $.post(url, post_data, function(data) {
            if (data == "added") {
                $(link).addClass('watchlist-active');
                // remove from history and blocklist
                $('#movie-'+movie_id+' .add-remove-history').removeClass('history-active');
                $('#movie-'+movie_id+' .add-remove-blocklist').removeClass('blocklist-active');
            } else if (data == "removed") {
                $(link).removeClass('watchlist-active');
            }
            $(link).html(content);
        }).fail(function() {
            $(link).html('<i class="fa fa-exclamation-triangle"></i>');
        }).always(function() {
            $(link).blur();
            $(link).tooltip('hide');
        });
        return false;
    });
    
    // ADD/REMOVE BLOCKLIST
    $('.add-remove-blocklist').click(function(e) {
        e.preventDefault();
        var link = this;
        var content = $(link).html();
        $(link).html('<i class="fa fa-spinner fa-spin"></i>');
        var movie_id = $(this).data('movieId');
        var url = "/ajax/blocklist_add_remove";
        var csrftoken = getCookie('csrftoken');
        var post_data = {
            'movie_id': movie_id,
            'csrfmiddlewaretoken': csrftoken,
        };
        $.post(url, post_data, function(data) {
            if (data == "added") {
                $(link).addClass('blocklist-active');
                // remove from history and watchlist
                $('#movie-'+movie_id+' .add-remove-history').removeClass('history-active');
                $('#movie-'+movie_id+' .add-remove-watchlist').removeClass('watchlist-active');
            } else if (data == "removed") {
                $(link).removeClass('blocklist-active');
            }
            $(link).html(content);
        }).fail(function() {
            $(link).html('<i class="fa fa-exclamation-triangle"></i>');
        }).always(function() {
            $(link).blur();
            $(link).tooltip('hide');
        });
        return false;
    });
    
    // ADD MOVIE
    $('.add-movie-ajax').click(function(e) {
        e.preventDefault();
        var link = this;
        var movie_id = $(this).data('movieId');
        var container = $('#add-movie-ajax-'+movie_id);
        $(container).html('<i class="fa fa-spinner fa-spin"></i>');
        var url = "/ajax/movie_save";
        var csrftoken = getCookie('csrftoken');
        var post_data = {
            'movie_id': movie_id,
            'csrfmiddlewaretoken': csrftoken,
        };
        $.post(url, post_data, function(data) {
            if (data == 'saved') {
                $(container).html('<a href="/movie/'+movie_id+'"><span class="glyphicon glyphicon-ok"></span></a>');
            } else {
            }
        });
        return false;
    });
    
    // UPDATE MOVIE
    $('.update-movie-ajax').click(function(e) {
        e.preventDefault();
        var link = this;
        var movie_id = $(this).data('movieId');
        $(link).html('<i class="fa fa-spinner fa-spin"></i>');
        var url = "/ajax/movie_update";
        var csrftoken = getCookie('csrftoken');
        var post_data = {
            'movie_id': movie_id,
            'csrfmiddlewaretoken': csrftoken,
        };
        $.post(url, post_data, function(data) {
            if (data == 'updated') {
                // reload page
                location.reload();
            } else {
                $(link).html('<i class="fa fa-exclamation-triangle"></i>');
            }
        }).fail(function() {
            $(link).html('<i class="fa fa-exclamation-triangle"></i>');
        });
        return false;
    });
    
    // ADD WATCHLIST IMPORTANT
    $('.add-important').click(function(e) {
        e.preventDefault();
        var link = this;
        $(link).html('<i class="fa fa-spinner fa-spin"></i>');
        var movie_id = $(link).data('movieId');
        var url = "/ajax/watchlist_important";
        var csrftoken = getCookie('csrftoken');
        var post_data = {
            'movie_id': movie_id,
            'csrfmiddlewaretoken': csrftoken,
        };
        $.post(url, post_data, function(data) {
            if (data == "added") {
                $(link).html('<i class="fa fa-star"></i>');
                $('#movie-poster').addClass('important');
            } else if (data == "removed") {
                $(link).html('<i class="fa fa-star-o"></i>');
                $('#movie-poster').removeClass('important');
            } else {
                $(link).html('<i class="fa fa-exclamation-triangle"></i>');
            }
        }).fail(function() {
            $(link).html('<i class="fa fa-exclamation-triangle"></i>');
        });
        return false;
    });
    
    // SEARCH FORM AUTOCOMPLETE
    $("#search-form").bind("keyup click", function() {
        var query = $(this).val();
        if (query.length >= 2) {
            $('#search-loading').show();
            var url = "/ajax/autocomplete";
            var csrftoken = getCookie('csrftoken');
            var post_data = {
                'query': query,
                'csrfmiddlewaretoken': csrftoken
            };
            $.post(url, post_data, function(data) {
                if (data == "empty") {
                    $("#search-results").hide();
                } else {
                    if (data) {
                        $('#search-results').html(data);
                        $('#search-results').show();
                    }
                }
                $('#search-loading').hide();
            });
        } else {
            $("#search-results").hide();
        }
    });
    $(document).click(function(e) {
        if (!$(e.target).is("#search-results")) {
            $("#search-results").hide();
        }
    });
    
    // CHANGE ORDER
    $('.change-order').change(function() {
        var order = $(this).val();
        if (order) {
            var url = "/discover?order=" + order;
            window.location = url;
        }
    });
    
    // CHANGE YEAR
    $('.change-year').change(function() {
        var year = $(this).val();
        if (year) {
            var url = "/discover?year=" + year;
            window.location = url;
        }
    });
    
    // TOOLTIPS
    $('.add-remove-history').tooltip();
    $('.add-remove-watchlist').tooltip();
    //$('.movie-poster').tooltip();
    
    $('.add-movie-link').tooltip({
        title: 'Add a Movie',
        placement: 'bottom',
        container: 'body',
    });
    
    $('.person-tooltip').tooltip({
        placement: 'top',
        container: 'body',
    });
    
    /*
    $('.add-important').tooltip({
        title: 'Add as important',
        placement: 'right',
        container: 'body',
    });
    */
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
