<div class="item card m-2 draggable infinite-item real-frame col-xs-6" v-bind:b_slug="book_slug" style="max-width:200px;"> 
    <div class="frame">
        <img v-bind:src="book_cover_url" v-if="book_cover_url != ''" v-bind:alt="book_title+'cover'" class="img-fluid">
        <img src="/HistMat/media/no_image.jpg" v-else v-bind:alt="book_title+' has no cover image'" class="img-fluid">
        
        <div class = "details jumbotron d-flex align-items-center">
            <div class="container">
                <a v-if="book_file_url != ''" class="btn btn-primary align-middle text-white bg-transparent bold file-button valid" v-bind:href="book_file_url" style="border: white 3px solid;">
                    <span style="font-size:large;">File</span>
                </a> 
                <a v-else class="btn btn-primary align-middle text-white bg-transparent bold file-button invalid" href="#" style="border: white 3px solid;">
                    <span style="font-size:large;">No File</span>
                </a>
                
            </div>
        </div>
    </div>
    
    <div class="detailed-details bg-white">
        <div class="p-1">
            <a v-bind:href="book_detail_url" >
                <span class="book-info">[[book_title]]</span>
            </a>
            <div >
                <span class="book-info">By [[book_author]]</span>
            </div>
        </div>
        
    </div>
    <div class="extended-details p-1 ">
        <span>More info</span>
    </div>
</div >