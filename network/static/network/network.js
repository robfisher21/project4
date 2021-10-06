

document.addEventListener('DOMContentLoaded', function() {
    
   // let url = window.location.href 
   // console.log(url)

    document.querySelectorAll("[id*='likebutton']").forEach(likebutton => {

        getlikes(likebutton.dataset.post, likebutton.dataset.status);
       
        likebutton.onclick = function() {

            fetch(`/like/${this.dataset.post}`, {
                method: 'POST',
                body: JSON.stringify({
                    likestatus: this.dataset.status,
                    post_id: this.dataset.post
                  })
                })
            
            .then (response => {
             //Evaluate whether the response returns error
                    if (response.ok)  {
                      return response.json();
                    } else; {
                      response.json();
          
                      
                      throw new Error ("Error loading likes"); 
                    }
                  })
          //  .then(response => response.json())

            .then(data => {

                console.log(data.message + data.post + "<< from server")
                document.querySelector(`#likebutton-${data.post}`)
                .setAttribute("data-status",data.message)
                document.querySelector(`#likecount-${data.post}`)
                .innerHTML=` ${data.likecount}`
                

                displaylikes(this.dataset.post, this.dataset.status);

                })

        }});

        
    });

    function getlikes (post) {

        fetch(`/like/${post}`)

        .then (response => {
            //Evaluate whether the response returns error
                   if (response.status)  {
                     return response.json();
                   } else; {
                     response.json();
         
                     
                     throw new Error ("Error loading likes"); 
                   }
                 })

        .then(data => {

            console.log(data.message + data.post + "<< from server")
            document.querySelector(`#likebutton-${data.post}`)
            .setAttribute("data-status",data.message)
      //      document.querySelector(`#likecount-${data.post}`)
      //      .innerHTML=` ${data.likecount}`

            return data

            })

        .then(data => {
            displaylikes(data.post, data.message);
  
            })
        
    }


    function displaylikes(post, status) {
        let likebutton = document.querySelector(`#heartlike-${post}`)
        let unlikebutton = document.querySelector(`#heartunlike-${post}`)

        if (status == "True") { 
        // Display Liked and hide Unliked button:
        likebutton.style.display = 'inline';
        unlikebutton.style.display = 'none';
        
     //   console.log('Unliked > LIKED')

        }
        else {
        // Display Unlike and Hide Like button
        likebutton.style.display = 'none';
        unlikebutton.style.display = 'inline';
        
      //  console.log('Liked > UNLIKED')

        }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

