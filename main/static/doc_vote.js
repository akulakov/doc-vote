
$( document ).ready(function() {

    function vote(event) {
        let page = $('.page').attr('id');
        let id = $(this).attr('id');
        let url = '/'+page+'/vote/'+id+'/'+event.data.dir+'/';
        let $this = $(this);

        $.ajax({ 'type':'POST', 'url':url }).done(function(data) {
            let val = $this.parent().find('.val');

            if (data.score < 0) {
                val.removeClass('green');
                val.addClass('red');
                val.text(data.score);
            }
            if (data.score > 0) {
                val.removeClass('red');
                val.addClass('green');
                val.text('+' + data.score);
            }
            if (data.score == 0) {
                val.text('');
            }

        });
    }
    $('.vote-down').click({ 'dir':0 }, vote);
    $('.vote-up').click({ 'dir':1 }, vote);

    $('.edit').click(function() {
        let $this = $(this);
        $this.hide();
        $this.parent().find('.save').show();
        let content = $(this).parent().find('.node-content');
        let id = $(this).attr('id');
        let url = '/ajax-node/'+id+'/';
        $.ajax({ 'type':'GET', 'url':url }).done(function(data) {
            let content = $this.parent().find('.node-content');
            content.html('<textarea style="width:500px; height:80px">' + data.body + '</textarea>');
        });
    });

    $('.save').click(function() {
        let $this = $(this);
        $this.hide();
        $this.parent().find('.edit').show();
        let content = $(this).parent().find('.node-content textarea').val();
        let id = $(this).attr('id');
        let url = '/ajax-node/'+id+'/';
        $.post(url, {'body': content}).done(function(data) {
            let content = $this.parent().find('.node-content');
            content.html(data.body);
            //content.contents().unwrap();
        });
    });

    $('.delete').click(function() {
        let $this = $(this);
        let id = $(this).attr('id');
        let url = '/ajax-node/'+id+'/';
        $this.parent().parent().css('background-color', '#966');
        let yes = confirm("Delete highlighted node? All of node's comments and votes will also be permanently deleted.");
        if (yes) {
            $.ajax({'type':'delete', 'url':url}).done(function(data) {
                $this.parent().parent().remove();
            });
        }
    });

});
