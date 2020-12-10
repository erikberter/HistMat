
ACTION_LIST = (
    ('book_add', 'Book Added'),
    ('book_rate', 'Book Rated'),
    ('book_page_change', 'Book Page Changed'), 
    ('post_add', 'Post Added'),
    ('post_comment', 'Post Commented'),
    ('post_like', 'Post liked'),
    ('apunte_add','Apunte added')
    )
ACTION_LIST_DICT = {
    'book_add' : {
        'text_b' : "~user~ ha aniadido el libro ~titulo~",
        'text' : {
            'es' : "{0} ha aniadido el libro {1}",
            'en' : "{0} has added the book {1}",
            'eu' : "{0} aniaditu du liburua {1}",
        }
    }, 
    'book_state' : {
        'text_b' : "~user~ ha aniadido el libro ~titulo~ a la estanteria ~estado~",
        'text' : {
            'es' : "{0} ha aniadido el libro {1} a la estanteria {2}",
            'en' : "{0} has added the book {1} to the shelf {2}",
            'eu' : "{0} aniaditu du liburua {1} {2} estanteriara",
        }
    }, 
    'book_rate' : {
        'text_b' : "~user~ ha valorado el libro ~titulo~ con ~puntuacion~",
        'text' : {
            'es' : "{0} ha valorado el libro {1} con {2}",
        }
    }, 
    'book_page_change' : {
        'text_b' : "~user~ ha avanzado en el libro ~titulo~ hasta la pagina ~pagina~",
        'text' : {
            'es' : "{0} ha avanzado en el libro {1} hasta la pagina {2}",
        }
    }, 
    'post_add' : {
        'text_b' : "~user~ ha aniadido un post: ~post~",
        'text' : {
            'es' : "{0} ha aniadido un post: {1}",
        }
    },
    'post_comment' : {
        'text_b' : "~user~ ha comentado en el post ~post~ : ~comentario~",
        'text' : {
            'es' : "{0} ha comentado en el post {1} : {2}",
        }
    },
    'post_like' : {
        'text_b' : "~user~ ha dado like al post ~post~",
        'text' : {
            'es' : "{0} ha dado like al post {1}",
        }
    },
    'apunte_add' : {
        'text_b' : "~user~ ha aniadido apunte ~apunte~",
        'text' : {
            'es' : "{0} ha aniadido apunte {1}",
        }
    }
}
