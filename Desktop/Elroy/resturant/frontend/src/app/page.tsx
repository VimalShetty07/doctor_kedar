'use client';

import { useState, useEffect } from 'react';
import Layout from '@/components/Layout';
import { Restaurant, MenuItem } from '@/types';
import api from '@/lib/api';
import { Star, Clock, MapPin } from 'lucide-react';

export default function HomePage() {
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [featuredItems, setFeaturedItems] = useState<MenuItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [restaurantRes, menuRes] = await Promise.all([
          api.get('/menu/restaurant'),
          api.get('/menu/items?available_only=true')
        ]);
        
        setRestaurant(restaurantRes.data);
        setFeaturedItems(menuRes.data.slice(0, 6)); // Show first 6 items
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      {/* Hero Section */}
      {restaurant?.banner_url && (
        <div className="relative h-96 mb-8">
          <img
            src={restaurant.banner_url}
            alt={restaurant.name}
            className="w-full h-full object-cover rounded-lg"
          />
          <div className="absolute inset-0 bg-black bg-opacity-40 rounded-lg flex items-center justify-center">
            <div className="text-center text-white">
              <h1 className="text-4xl font-bold mb-4">{restaurant.name}</h1>
              {restaurant.description && (
                <p className="text-xl max-w-2xl mx-auto">{restaurant.description}</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Restaurant Info */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {restaurant?.name || 'Restaurant'}
            </h2>
            {restaurant?.address && (
              <div className="flex items-center text-gray-600 mb-2">
                <MapPin className="h-4 w-4 mr-2" />
                {restaurant.address}
              </div>
            )}
            {restaurant?.phone && (
              <div className="flex items-center text-gray-600">
                <Clock className="h-4 w-4 mr-2" />
                Open Now • {restaurant.phone}
              </div>
            )}
          </div>
          {restaurant?.logo_url && (
            <img
              src={restaurant.logo_url}
              alt="Logo"
              className="h-16 w-16 object-contain"
            />
          )}
        </div>
      </div>

      {/* Featured Menu Items */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Featured Items</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featuredItems.map((item) => (
            <div
              key={item.id}
              className="bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition-shadow"
            >
              {item.image_url && (
                <img
                  src={item.image_url}
                  alt={item.name}
                  className="w-full h-48 object-cover"
                />
              )}
              <div className="p-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {item.name}
                </h3>
                {item.short_description && (
                  <p className="text-gray-600 text-sm mb-3">
                    {item.short_description}
                  </p>
                )}
                <div className="flex items-center justify-between">
                  <span className="text-lg font-bold text-blue-600">
                    ₹{item.price}
                  </span>
                  <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 text-sm">
                    Add to Cart
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Call to Action */}
      <div className="bg-blue-600 text-white rounded-lg p-8 text-center">
        <h2 className="text-2xl font-bold mb-4">Ready to Order?</h2>
        <p className="text-blue-100 mb-6">
          Browse our full menu and place your order online
        </p>
        <a
          href="/menu"
          className="bg-white text-blue-600 px-6 py-3 rounded-md font-semibold hover:bg-gray-100 transition-colors"
        >
          View Full Menu
        </a>
      </div>
    </Layout>
  );
}
