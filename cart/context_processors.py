from . cart import Cart

# create context processors and it will work on all pages
def cart(request):
    # return default data from our cart
    return {'cart':Cart(request)}