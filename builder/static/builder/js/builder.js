    $(document).ready( function () {
		$('.table > tbody  > tr').each( function () {
			var td_id = $(this).children()[0]
			$('.table > thead > tr > th').first().hide()
			hideId(td_id)
			var word_id = td_id.innerText
			var edit_ref = $(this).find('.edit')[0]
			const url = "edit/" + word_id + "/"
			$(edit_ref).attr("href", url)
		})

		var paginatorNav = $(".table-container").find('nav')
		modifyPaginationStyle( paginatorNav )

	})
	$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE') {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    }
	});
    $(".delete").click(function () {
		var row = $(this).parent().parent().parent()
        var word_id_to_delete = $(this).parent().parent().siblings()[0].innerText
		const url_to_delete = "delete/"

		$.ajax({
			type: "POST",
			url: url_to_delete,
			data: {
          	'word': word_id_to_delete
        	},
			dataType: 'json',
			success: function (data) {
				if (data.is_deleted) {
					row.hide("slow")
				}
			}
    	});
	});
	
	function hideId(td) {
		$(td).hide()
	}

	function modifyPaginationStyle(paginatorNav) {
		var li_s = $(paginatorNav).find(".pagination").children('li')
		li_s.each( function () {
			$(this).addClass("page-item")
			$(this).first('a').addClass("page-link")
		})

	}