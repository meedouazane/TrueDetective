$(document).ready(function () {
    $('#videoForm').submit(function (event) {
        event.preventDefault();

        let url = '';
        if ($('#Check').is(':checked')) {
            url = 'http://127.0.0.1:5000/check';
        } else if ($('#Translate').is(':checked')) {
            url = 'http://127.0.0.1:5000/translate';
        } else if ($('#Convert').is(':checked')) {
            url = 'http://127.0.0.1:5000/convert';
        }
        const youtubeUrl = $('#youtubeUrl').val();
        const formData = new FormData();
        $('#spinner').show();
        if (youtubeUrl) {
            formData.append('url', youtubeUrl);
        }

        $.ajax({
            method: 'POST',
            url: url,
            dataType: 'json',
            processData: false,
            contentType: false,
            data: formData,
            success: function (response) {
                $('#spinner').hide();
                $('#description').text(response.Result);
                $('#download_links').empty();
                if ($('#Check').is(':checked')) {
                    $('#title_case').html('&darr;&darr;&darr; Checking for Misinformation &darr;&darr;&darr;');
                    $('#download_links').html('<a id="check" href="/tmp_Result/checking.pdf">Check File in PDF</a><br />');
                } else if ($('#Translate').is(':checked')) {
                    $('#title_case').html('&darr;&darr;&darr;Translation for this video &darr;&darr;&darr;');
                    $('#download_links').html('<a id="translate_link" href="/tmp_Result/translation.pdf">Translation File in PDF</a><br />');
                    $('#download_links').append('<a id="translate_link2" href="/Translated_Audio/myAudio.mp3">Translation File in mp3</a><br />');
                } else if ($('#Convert').is(':checked')) {
                    $('#download_links').html('<a id="convert_link" href="/tmp_Audio/myAudio.mp3">Download mp3</a><br />');
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                $('#spinner').hide();
                $('#description').text('Error: ' + textStatus + ' - ' + errorThrown);
            }
        });
    });

    $('#cancelButton').click(function () {
        $('#videoForm')[0].reset();
        $('#description').text('');
        $('#download_links').empty();
        $('#spinner').hide();
    });
    });