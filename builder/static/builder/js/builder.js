    $(document).ready( function () {
		$('.table > tbody  > tr').each( function () {
			var td_id = $(this).children()[0]
			$('.table > thead > tr > th').first().hide()
			hideId(td_id)
			var word_id = td_id.innerText

			var edit_ref = $(this).find('.edit')[0]
			var meanings_ref = $(this).find('.meanings-ref')[0]
			var examples_ref = $(this).find('.examples-ref')[0]

			const edit_url = "edit/" + word_id + "/"
			const meanings_url = word_id + "/meanings/"
			const examples_url = word_id + "/examples/"

			$(edit_ref).attr("href", edit_url)
			$(meanings_ref).attr("href", meanings_url)
			$(examples_ref).attr("href", examples_url)
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