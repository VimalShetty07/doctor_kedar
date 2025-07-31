'use client';

import { useState, useEffect } from 'react';
import Layout from '@/components/Layout';
import { MenuItem } from '@/types';
import api from '@/lib/api';
import toast from 'react-hot-toast';
import { Plus, Minus, ShoppingCart } from 'lucide-react';

export default function MenuPage() {
  const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [quantities, setQuantities] = useState<{ [key: number]: number }>({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [itemsRes, categoriesRes] = await Promise.all([
          api.get('/menu/items?available_only=true'),
          api.get('/menu/categories')
        ]);
        
        setMenuItems(itemsRes.data);
        setCategories(categoriesRes.data);
      } catch (error) {
        console.error('Error fetching menu:', error);
        toast.error('Failed to load menu');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const filteredItems = selectedCategory
    ? menuItems.filter(item => item.category === selectedCategory)
    : menuItems;

  const handleQuantityChange = (itemId: number, change: number) => {
    const currentQuantity = quantities[itemId] || 0;
    const newQuantity = Math.max(0, currentQuantity + change);
    
    if (newQuantity === 0) {
      const newQuantities = { ...quantities };
      delete newQuantities[itemId];
      setQuantities(newQuantities);
    } else {
      setQuantities({ ...quantities, [itemId]: newQuantity });
    }
  };

  const handleAddToCart = async (item: MenuItem) => {
    const quantity = quantities[item.id] || 1;
    
    try {
      await api.post('/cart/add', {
        menu_item_id: item.id,
        quantity: quantity
      });
      
      toast.success(`${quantity}x ${item.name} added to cart!`);
      setQuantities({ ...quantities, [item.id]: 0 });
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to add to cart');
    }
  };

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
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Our Menu</h1>
        
        {/* Category Filter */}
        <div className="flex flex-wrap gap-2 mb-6">
          <button
            onClick={() => setSelectedCategory('')}
            className={`px-4 py-2 rounded-md text-sm font-medium ${
              selectedCategory === ''
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            All Items
          </button>
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 rounded-md text-sm font-medium ${
                selectedCategory === category
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {/* Menu Items Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredItems.map((item) => (
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
                <div className="flex items-center justify-between mb-3">
                  <span className="text-lg font-bold text-blue-600">
                    ₹{item.price}
                  </span>
                  {item.category && (
                    <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                      {item.category}
                    </span>
                  )}
                </div>
                
                {/* Quantity Controls */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleQuantityChange(item.id, -1)}
                      className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center hover:bg-gray-300"
                    >
                      <Minus className="h-4 w-4" />
                    </button>
                    <span className="w-8 text-center">
                      {quantities[item.id] || 0}
                    </span>
                    <button
                      onClick={() => handleQuantityChange(item.id, 1)}
                      className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center hover:bg-gray-300"
                    >
                      <Plus className="h-4 w-4" />
                    </button>
                  </div>
                  
                  <button
                    onClick={() => handleAddToCart(item)}
                    disabled={!quantities[item.id]}
                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-1"
                  >
                    <ShoppingCart className="h-4 w-4" />
                    <span>Add</span>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredItems.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">
              No items found in this category.
            </p>
          </div>
        )}
      </div>
    </Layout>
  );
} 