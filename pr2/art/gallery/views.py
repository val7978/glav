from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Artwork, Favorite, Cart, Order, OrderItem
from .forms import ContactForm

def general(request):
    featured_artworks = Artwork.objects.filter(is_featured=True)[:4]
    new_artworks = Artwork.objects.order_by('-created_at')[:8]
    summer_artworks = Artwork.objects.filter(category__name__icontains='лето')[:3]
    abstract_artworks = Artwork.objects.filter(category__name__icontains='абстракция')[:3]
    
    context = {
        'featured_artworks': featured_artworks,
        'new_artworks': new_artworks,
        'summer_artworks': summer_artworks,
        'abstract_artworks': abstract_artworks,
    }
    return render(request, 'general.html', context)

@login_required
def likes(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('artwork')
    artworks = [fav.artwork for fav in favorites]
    return render(request, 'likes.html', {'artworks': artworks})

@login_required
def korzina(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('artwork')
    total_price = sum(item.artwork.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        if 'update' in request.POST:
            for item in cart_items:
                new_quantity = int(request.POST.get(f'quantity_{item.id}', 1))
                if new_quantity > 0:
                    item.quantity = new_quantity
                    item.save()
                else:
                    item.delete()
            messages.success(request, "Корзина обновлена")
            return redirect('korzina')
        
        elif 'checkout' in request.POST:
            order = Order.objects.create(
                user=request.user,
                total_price=total_price
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    artwork=item.artwork,
                    quantity=item.quantity,
                    price=item.artwork.price
                )
            cart_items.delete()
            messages.success(request, "Заказ успешно оформлен!")
            return redirect('dashboard')
    
    return render(request, 'korzina.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def toggle_favorite(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        artwork=artwork
    )
    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed', 'count': request.user.favorites.count()})
    return JsonResponse({'status': 'added', 'count': request.user.favorites.count()})

@login_required
def add_to_cart(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        artwork=artwork,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return JsonResponse({
        'status': 'success',
        'count': Cart.objects.filter(user=request.user).count()
    })

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Товар удален из корзины")
    return redirect('korzina')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваше сообщение отправлено!")
            return redirect('general')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

from django.shortcuts import render
from .models import Artwork, Category

def home(request):
    categories = Category.objects.all()
    new_artworks = Artwork.objects.order_by('-created_at')[:8]
    
    context = {
        'categories': categories,
        'new_artworks': new_artworks,
    }
    return render(request, 'general.html', context)

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def add_to_favorites(request, artwork_id):
    artwork = Artwork.objects.get(id=artwork_id)
    Favorite.objects.get_or_create(user=request.user, artwork=artwork)
    return JsonResponse({'status': 'added'})

@login_required
def add_to_cart(request, artwork_id):
    artwork = Artwork.objects.get(id=artwork_id)
    Cart.objects.get_or_create(user=request.user, artwork=artwork)
    return JsonResponse({'status': 'added'})














