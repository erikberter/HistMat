
<li class="item card m-2 draggable infinite-item real-frame col-xs-6 shadow moving-element" v-bind:b_slug="book_slug" style="max-width:200px;"> 
    <div class="frame">
        <img v-bind:src="book_cover_url" v-if="book_cover_url != ''" v-bind:alt="book_title+'cover'" class="img-fluid">
        <img src="/HistMat/media/no_image.jpg" v-else v-bind:alt="book_title+' has no cover image'" class="img-fluid">
        
        <div class = "details jumbotron d-flex align-items-center">
            <div class="container p-1 d-flex flex-column">
                <a v-if="book_file_url != ''" class="btn btn-primary align-middle text-white bg-transparent bold thumb-button file valid" v-bind:href="book_file_url" style="border: white 3px solid;">
                    <span style="font-size:large;"><i class="fa fa-file-pdf"></i> File</span>
                </a> 
                <a v-else class="btn btn-primary align-middle text-white bg-transparent bold thumb-button file invalid" href="#" style="border: white 3px solid;">
                    <span style="font-size:large;"><i class="fa fa-file-exclamation"></i> No File</span>
                </a>
                <a class="btn btn-primary align-middle text-white bg-transparent bold thumb-button search valid mt-1" v-bind:href="book_detail_url" style="border: white 3px solid;">
                    <span><i class="fa fa-search"></i> Detalles</span>
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
        <div class="d-flex flex-row">
            <span>Tags:</span>
            <div class="d-flex flex-row flex-wrap">
                <span class="badge badge-danger m-1" v-if="index<2" v-for="(tag, index) in book_tags">[[tag]]</span>
            </div>
        </div>
    </div>
</li >
</transition-group>