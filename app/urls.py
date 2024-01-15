from django.urls import path
from . import views

urlpatterns = [
    # path('/',views.index,name="index"),
    path('', views.getRoutes, name='getRouters'),
    path('products/', views.getProducts, name='getProducts'),
    path('products/<str:pk>/', views.ProductDetailView.as_view(), name='getProduct'),
    path('user/profile/', views.getUserProfiles, name="getUserProfiles"), 
    # path('products/<str:pk>/', views.getProduct, name='getProduct'),
    path('users/', views.getUsers, name="getUsers"),
    
    # path('products/search/', views.ProductSearchView.as_view(), name='product-search'),
    path('products/search/<str:keyword>', views.ProductSearchView.as_view(), name='product-search'),

    # path('products/search/', views.ProductSearchView.as_view(), name='product-search'),
    path('create-order/', views.create_order, name='create_order'), 
    path('get-order-id/', views.get_order_id, name='get_order_id'),

    path('get-user-orders/', views.get_user_orders, name='get-user-orders'),
    path('get-all-orders/', views.get_all_orders_view, name='get-all-orders'),
    
    path('delete-orders/<int:pk>/', views.delete_user_order, name='delete-order'),
    path('get-order-items/', views.get_order_items, name='get-order-items'),

    path('save-shipment/', views.save_shipment, name='save_shipment'),
    path('get-user-shipments/', views.get_user_shipments, name='get-user-shipments'),
    path('get-all-users-shipments/', views.get_all_user_shipments, name='get-all-user-shipments'),

    path('get-user-reviews/', views.get_user_reviews, name='get-user-reviews'),
    path('review-list/<int:product_id>/', views.review_list_view, name='review-list'),
    path('add-review/', views.add_review, name='add_review'),
    path('edit-review/<int:review_id>/', views.edit_review, name='edit_review'),

    path('confirm-order-delivery/<int:pk>/', views.confirm_order_delivery, name='confirm-order-delivery'),

    path('products/<int:pk>/track-product-view/<int:user_id>/', views.track_product_view, name='track-product-view'),

    path('products/<int:pk>/save-product/<int:user_id>/', views.save_product_to_favorites, name='save-product'),
    path('products/<int:pk>/remove-product/<int:user_id>/', views.remove_product_from_favorites, name='remove-product'),
    path('get-user-favorite-products/', views.get_user_favorite_products, name='user-favorite-products'),
    path('get-user-viewed-products/', views.get_user_viewed_products, name='user-favorite-products'),

]
