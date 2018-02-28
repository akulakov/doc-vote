
$( document ).ready(function() {
    let page = $('.page').attr('id');

    function vote(event) {
        let page = $('.page').attr('id');
        let id = $(this).attr('id');
        let url = '/'+page+'/vote/'+id+'/'+event.data.dir+'/';
        let $this = $(this);

        if (!$('.username').val()) alert('You need to login in order to vote.')

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

    $('#content').on('click', '.edit', function() {
        let $this = $(this);
        $this.hide();
        let $node = $this.parent().parent().parent().parent();
        $node.find('.save').show();
        let content = $node.find('.node-content');
        let id = $this.attr('id');
        let url = '/ajax-node/'+id+'/';
        $.ajax({ 'type':'GET', 'url':url }).done(function(data) {
            let content = $node.find('.node-content');
            content.html('<textarea style="width:500px; height:80px">' + data.body + '</textarea>');
        });
    });

    $('#content').on('click', '.save', function() {
        let $this = $(this);
        $this.hide();
        let $node = $this.parent();
        $node.find('.edit').show();

        let content = $node.find('.node-content textarea').val();
        let id = $(this).attr('id');
        let url = '/ajax-node/'+id+'/';
        $.post(url, {'body': content}).done(function(data) {
            let content = $node.find('.node-content');
            content.html(data.body);
        });
    });

    $('#content').on('click', '.delete', function() {
        let $this = $(this);
        let id = $(this).attr('id');
        let url = '/ajax-node/'+id+'/';
        let $node = $this.parent().parent().parent().parent();
        $node.css('background-color', '#f7cec0');
        setTimeout(function() {
            let yes = confirm("Delete highlighted node? All of node's comments and votes will also be permanently deleted.");
            if (yes) {
                $.ajax({'type':'delete', 'url':url}).done(function(data) {
                    $node.remove();
                });
            }
            $this.node.css('background-color', '#fff');

        }, 50);
    });

    $('#content').on('click', '.add-node', function() {
        let $this = $(this);
        let id = $this.attr('id');
        let $node = $this.parent().parent().parent().parent();
        let $div = $node.after('<div class="new-node"><h4>New Node</h4><textarea id='+id+
            '></textarea><div class="clear"></div><button class="save-new left">Save</button>'+
            '<button class="cancel-add left" href="#">Cancel</button></div><div class="clear"></div>');
        setTimeout(function() {
            $div.find('textarea').focus();
        }, 50);
        $('#content').on('click', 'button.cancel-add', function() {
            $('.new-node').remove()
        });

        $('#content').on('click', 'button.save-new', function() {
            let $this = $(this);
            let ta = $this.parent().find('textarea');
            let id = ta.attr('id');
            let url = '/'+page+'/ajax-create-update-node/'+id+'/after/';

            $.post(url, {'body': ta.val()}).done(function(data) {
                $('div.new-node').replaceWith(data.body);
            });
        });


    });

    $(document).on('mouseenter', '.actions', function () {
        $(this).find(".inner").show();
        $(this).find(".act-hover").hide();
        }).on('mouseleave', '.actions', function () {
            $(this).find(".inner").hide();
            $(this).find(".act-hover").show();
        });


});
