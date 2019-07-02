$(document).ready(function(){
  var contactForm=$('.contact-form')
  var contactFormMethod=contactForm.attr('method')
  var contactFormEndPoint=contactForm.attr('action')

  function doingSubmitting(submitBtn,defaultText,doSubmit){
    if (doSubmit){
      submitBtn.addClass('disabled')
      submitBtn.html("<i class='fa fa-spin fa-spinner'></i>Sending....")
    }
    else{
      submitBtn.removeClass('disabled')
      submitBtn.html(defaultText)
    }

  }
  contactForm.submit(function(event) {
    event.preventDefault()
    var contactFormSubmitButton=contactForm.find("[type='submit']")
    var contactFormSubmitButtontxt=contactFormSubmitButton.text()
    var contactFormData=contactForm.serialize()
    var thisForm=$(this)
    doingSubmitting(contactFormSubmitButton,'',true)
  $.ajax({
    url:contactFormEndPoint,
    method:contactFormMethod,
    data:contactFormData,
    success:function(data) {
        contactForm[0].reset()
        $.alert({
          title: 'Yahoo !!',
          content:data.message,
          theme: 'supervan',
      })
      setTimeout(function() {
        doingSubmitting(contactFormSubmitButton,contactFormSubmitButtontxt,false)
      },3000)
    },
    error:function(error) {
      // console.log(error.responseJSON);
      var jsonData=error.responseJSON
      var msg=''
      $.each(jsonData,function(key,value) {
        msg+=key+" : "+value[0].message+ "</br>"
      })
      $.alert({
        title: 'OMG!!',
        content: msg,
        theme: 'supervan',
    })
    setTimeout(function() {
      doingSubmitting(contactFormSubmitButton,contactFormSubmitButtontxt,false)
    },2000)
  }
  })
})

  //search methods using Ajax
  var searchForm=$('.search-form')
  var searchInput=searchForm.find("[name='q']")
  var typeTimer;
  var typeInterval=500 //milliseconds
  var searchButton=searchForm.find("[type='submit']")
  searchInput.keyup(function(event){
    clearTimeout(typeTimer)
    typeTimer=setTimeout(doSearch,typeInterval)
  })

  searchInput.keydown(function(event){
    clearTimeout(typeTimer)
  })
  function doingSearch(){
    searchButton.addClass('disabled')
    searchButton.html("<i class='fa fa-spin fa-spinner'></i>Searching....")
  }

  function doSearch(){
    doingSearch()
    var query=searchInput.val()
    setTimeout(function(){
      window.location.href='/search/?q='+query
    },1000)

  }

  // Cart Ajax Updates
  var productForm=$('.form-product-ajax')
  productForm.submit(function(event){
    event.preventDefault();
    var thisForm=$(this);
    var actionUrl=thisForm.attr('data-endpoint');
    var httpMethod=thisForm.attr('method');
    var formData=thisForm.serialize();


    // Ajax Call to Introduce Asynchronous Functinaltiy
    $.ajax({
      url:actionUrl,
      method:httpMethod,
      data:formData,
      success:function(data){
        console.log('success')
        console.log(data)
        var submitSpan=thisForm.find('.submit-span')
        if(data.added){
          submitSpan.html('<b>Already Added</b><button type="submit" class="btn btn-link">Remove</button>')
        }
        else{
          submitSpan.html('<button type="submit" class="btn btn-success">Add to Cart</button>')
        }
        var cartCount=$('.navbar-count')
        cartCount.text(data.cartUpdateCount)
        var currentPath=window.location.href

        if (currentPath.indexOf('cart')!=-1){
          refreshCart()
        }

      },
      error:function(errorData){
        $.alert({
          title: 'OMG!!',
          content: 'Encounter error please check again',
          theme: 'supervan',
        })
      }
    })
  })
  function refreshCart(){
      var cartTable = $('.cart-table')
      var cartBody = cartTable.find('.cart-body')
      var productRows=cartBody.find('.cart-product')
      var currentUrl=window.location.href
      // cartBody.html('<h1>Cart Changed </h1>')
      var updateCartUrl='/api/cart';
      var UpdateCartMethod='GET';
      var data={};

      $.ajax({
        url:updateCartUrl,
        method:UpdateCartMethod,
        data:data,
        success:function(data){
          var hiddenCartRemoveItem=$('.cart-item-remove-form')
          console.log('success')
          console.log(data);
          if (data.products.length>0){
            productRows.html(' ')
            i=data.products.length
            $.each(data.products, function(index,value) {
              var newCartItemRemove=hiddenCartRemoveItem.clone()
              newCartItemRemove.css('display','block')
              // Remove the items which is present in the cart by assiging a remove form to current cart-id
              newCartItemRemove.find('.cart-item-product-id').val(value.id)
              cartBody.prepend("<tr><th scope=\"row\">" + i+ "</th><td><a href=' " +value.url+ "'> " +value.name+ "</a>"+newCartItemRemove.html()+" </td><td>" +value.price+ "</td></tr>?")
              i--
            })
            cartBody.find('.cart-subtotal').text(data.subtotal)
            cartBody.find('.cart-total').text(data.total)
          }
          else {
            window.location.href=currentUrl
          }

        },
        error:function(errorData){
          console.log('error')
          console.log(errorData)
        }
      })

}
})
