/*
        JQUERY UI FUNCTIONS
*/

/**
 * **Summary**. Refreshes the Sortable div.
 * 
 * **Description**. Creates a list of id's with all checked checkboxes in the filter sections
 *              and then makes the whole list of *div's* connected lists so one can drag 
 *              and drop between them.
 */
function refreshSortable(){
    var selected = [];
    $('.cb_filter_selector:checked').each(
        function() {
            selected.push("#sortable-" + this.id.substring(3));
        }
    ); 
    
    var selected_id_string =  selected.join();
    $(selected_id_string).sortable({
        connectWith: ".connectedSortable",
        dropOnEmpty: true,
        start: function() {
            memo = $(this).css('transition');
            $(this).css('transition', 'none');
          },
          stop: function() {
            $(this).css('transition', memo);
          },
        receive: function( event, ui ) {
            let book_state = $(this).attr('shelf_name').trim();
            let book_slug = ui.item.attr('b_slug').trim();
            console.log(book_slug);
            send_book_state_change_ajax(book_state, book_slug);
        }
    }).disableSelection();
}

/*
        ONLOAD JQUERY
*/
$(document).ready(function() {
    /**
     * **Summary**. On click listener for the filter menu toggle button.
     */
    $("#menu-toggle").click(function(e) {
        e.preventDefault();

        $("#wrapper").toggleClass("toggled");
        $("#menu-toggle i").toggleClass('fa-angle-double-left fa-angle-double-right');
      });
      
});

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"


// VUE COMPONENTS


Vue.component('modal_book_list', {
    template: '#modal_book_list',
    delimiters: ['[[', ']]'],
    props: ['book_state','shelf_title','books', 'search_query']
});

Vue.component('book_item', {
    template: '#modal_book',
    delimiters: ['[[', ']]'],
    props: ['book_slug','book_title','book_author', 'book_cover_url', 'book_file_url', 'book_detail_url', 'book_tags']
});


var catalog_app = new Vue({
    el: '#catalog-app',
    delimiters: ['[[', ']]'],
    data: {
        book_lists : [],
        active_book_states : [],
        search_query : ""
    },
    methods: {
        fab_action: function (event) {
            window.location = this.create_url;
        },
        load_books : function (book_state){
            if(this.active_book_states.includes(book_state)){
                for(var i = 0; i < this.active_book_states.length; i++){
                    if(book_state == this.active_book_states[i]){
                        this.active_book_states.splice(i,1);
                        this.book_lists.splice(i,1);
                    }
                }
                Vue.nextTick(function () {
                    refreshSortable();
                });
            }else{
                axios.post(window.location.pathname, {
                    book_state : book_state
                })
                .then(response => {

                    this.book_lists.push(response.data);
                    this.active_book_states.push(book_state);

                    console.log(this.book_lists);

                    $('#container-'+response.data.book_state).remove();
                    $('#book-to-add').append(response);

                    this.$nextTick(() => {
                        refreshSortable();
                    });
                    
                })
                .catch(error => {
                    console.log(error)
                });
            }
            
        },
        order_books : function(order_function){
            switch(order_function){
                case "last-added": 
                    for(var i = 0; i < this.book_lists.length; i++)
                        this.book_lists[i].books.sort(function(a,b){
                            return new Date(b.created) - new Date(a.created);
                        });
                    break;
                case "first-added":
                    for(var i = 0; i < this.book_lists.length; i++)
                        this.book_lists[i].books.sort(function(a,b){
                            return new Date(a.created) - new Date(b.created) ;
                        });
                    break;
                default:
                    console.error('Not valid order');
            }
        }
    },
    created : function(){
		this.load_books('Reading');
        $('#cb-reading').attr('checked','checked');
    }
})