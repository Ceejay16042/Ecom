var updateBtn = document.getElementsByClassName('update-cart')
// this code helps to interact with the add to cart button
for(var i = 0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)
// this code helps to keep in check if the user is authenticated
        
        console.log('USER:', user)
    
        if(user === 'AnonymousUser'){
            // updateUserOrder(productId, action)
            addCookieItem(productId, action)
            // updateUserOrder(productId, action)

            // console.log('Not logged in')
        }else{
            updateUserOrder(productId, action)
        }

    })
}
function addCookieItem(productId, action){
    console.log('Not logged in!')
    
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity': 1}
        }else{
            cart[productId]['quantity'] += 1
            console.log('cart was added!')
        }
    }
    if(action == 'remove'){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0){
            console.log('delete items')
            delete cart[productId]
        }
    }
    console.log('Cart', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}


// this is a fetch api used to send information concerning the productid , action to the database
function updateUserOrder(productId, action){
    console.log('User is logged in, sending data')

    var url = 'update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    
    // this code helps to send the json response in the views.py
    .then((response) =>{
        return response.json()
    })
    // this code helps to send the data to  the backend!
    .then((data => {
        console.log('data:', data)
    //  this code helps to make sure that the next data inputted gets to be displayed immediately it is been set
        location.reload()
    })
)} 

