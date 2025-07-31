'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Layout from '@/components/Layout';
import { Cart, Bill } from '@/types';
import api from '@/lib/api';
import toast from 'react-hot-toast';
import { MapPin, FileText } from 'lucide-react';

export default function CheckoutPage() {
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);
  const [placingOrder, setPlacingOrder] = useState(false);
  const [deliveryAddress, setDeliveryAddress] = useState('');
  const [specialInstructions, setSpecialInstructions] = useState('');
  const router = useRouter();

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const response = await api.get('/cart/');
      setCart(response.data);
    } catch (error) {
      console.error('Error fetching cart:', error);
      toast.error('Failed to load cart');
      router.push('/cart');
    } finally {
      setLoading(false);
    }
  };

  const handlePlaceOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!cart || cart.items.length === 0) {
      toast.error('Your cart is empty');
      return;
    }

    setPlacingOrder(true);
    try {
      const response = await api.post('/orders/place', {
        delivery_address: deliveryAddress,
        special_instructions: specialInstructions
      });
      
      toast.success('Order placed successfully!');
      router.push(`/orders/${response.data.id}`);
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to place order');
    } finally {
      setPlacingOrder(false);
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

  if (!cart || cart.items.length === 0) {
    router.push('/cart');
    return null;
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Checkout</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Order Form */}
          <div>
            <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Delivery Information</h2>
              
              <form onSubmit={handlePlaceOrder} className="space-y-4">
                <div>
                  <label htmlFor="address" className="block text-sm font-medium text-gray-700 mb-2">
                    Delivery Address
                  </label>
                  <div className="relative">
                    <MapPin className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                    <textarea
                      id="address"
                      value={deliveryAddress}
                      onChange={(e) => setDeliveryAddress(e.target.value)}
                      className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      rows={3}
                      placeholder="Enter your delivery address"
                      required
                    />
                  </div>
                </div>
                
                <div>
                  <label htmlFor="instructions" className="block text-sm font-medium text-gray-700 mb-2">
                    Special Instructions (Optional)
                  </label>
                  <textarea
                    id="instructions"
                    value={specialInstructions}
                    onChange={(e) => setSpecialInstructions(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    rows={2}
                    placeholder="Any special instructions for your order"
                  />
                </div>
                
                <button
                  type="submit"
                  disabled={placingOrder}
                  className="w-full bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
                >
                  {placingOrder ? 'Placing Order...' : 'Place Order'}
                </button>
              </form>
            </div>
          </div>

          {/* Order Summary */}
          <div>
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Order Summary</h2>
              
              {/* Cart Items */}
              <div className="space-y-3 mb-6">
                {cart.items.map((item) => (
                  <div key={item.id} className="flex justify-between items-center">
                    <div className="flex items-center space-x-3">
                      <span className="text-sm text-gray-500">×{item.quantity}</span>
                      <span className="font-medium">
                        {item.menu_item?.name || 'Unknown Item'}
                      </span>
                    </div>
                    <span className="font-medium">
                      ₹{item.quantity * item.price_at_time}
                    </span>
                  </div>
                ))}
              </div>
              
              {/* Price Breakdown */}
              <div className="border-t pt-4 space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">Subtotal</span>
                  <span>₹{cart.subtotal}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">CGST (9%)</span>
                  <span>₹{(cart.subtotal * 0.09).toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">SGST (9%)</span>
                  <span>₹{(cart.subtotal * 0.09).toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-lg font-bold border-t pt-2">
                  <span>Total</span>
                  <span className="text-blue-600">
                    ₹{(cart.subtotal * 1.18).toFixed(2)}
                  </span>
                </div>
              </div>
              
              <div className="mt-6 p-4 bg-blue-50 rounded-md">
                <div className="flex items-center space-x-2 text-blue-800">
                  <FileText className="h-5 w-5" />
                  <span className="font-medium">Important Note</span>
                </div>
                <p className="text-sm text-blue-700 mt-2">
                  This is a demo application. No actual payment will be processed. 
                  You will receive a bill with GST calculation after placing your order.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
} 