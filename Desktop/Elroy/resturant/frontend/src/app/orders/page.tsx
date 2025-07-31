'use client';

import { useState, useEffect } from 'react';
import Layout from '@/components/Layout';
import { Order } from '@/types';
import api from '@/lib/api';
import toast from 'react-hot-toast';
import { Clock, MapPin, FileText } from 'lucide-react';
import Link from 'next/link';

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const response = await api.get('/orders/');
      setOrders(response.data);
    } catch (error) {
      console.error('Error fetching orders:', error);
      toast.error('Failed to load orders');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'confirmed':
        return 'bg-blue-100 text-blue-800';
      case 'preparing':
        return 'bg-orange-100 text-orange-800';
      case 'ready':
        return 'bg-green-100 text-green-800';
      case 'delivered':
        return 'bg-gray-100 text-gray-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
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
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Your Orders</h1>
        
        {orders.length === 0 ? (
          <div className="text-center py-12">
            <Clock className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">No orders yet</h2>
            <p className="text-gray-600 mb-6">Start by browsing our menu and placing your first order!</p>
            <Link
              href="/menu"
              className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700"
            >
              Browse Menu
            </Link>
          </div>
        ) : (
          <div className="space-y-6">
            {orders.map((order) => (
              <div key={order.id} className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      Order #{order.order_number}
                    </h3>
                    <p className="text-sm text-gray-600">
                      {new Date(order.created_at).toLocaleDateString()} at{' '}
                      {new Date(order.created_at).toLocaleTimeString()}
                    </p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(order.status)}`}>
                    {order.status}
                  </span>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Order Items</h4>
                    <div className="space-y-1">
                      {order.items.map((item) => (
                        <div key={item.id} className="flex justify-between text-sm">
                          <span>
                            {item.quantity}x {item.menu_item?.name || 'Unknown Item'}
                          </span>
                          <span>₹{item.total_price}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Order Details</h4>
                    <div className="space-y-1 text-sm">
                      <div className="flex justify-between">
                        <span>Subtotal:</span>
                        <span>₹{order.subtotal}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>CGST (9%):</span>
                        <span>₹{order.cgst_amount}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>SGST (9%):</span>
                        <span>₹{order.sgst_amount}</span>
                      </div>
                      <div className="flex justify-between font-semibold border-t pt-1">
                        <span>Total:</span>
                        <span className="text-blue-600">₹{order.total_amount}</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                {order.delivery_address && (
                  <div className="mb-4">
                    <div className="flex items-center space-x-2 text-gray-600 mb-1">
                      <MapPin className="h-4 w-4" />
                      <span className="text-sm font-medium">Delivery Address</span>
                    </div>
                    <p className="text-sm text-gray-700">{order.delivery_address}</p>
                  </div>
                )}
                
                {order.special_instructions && (
                  <div className="mb-4">
                    <div className="flex items-center space-x-2 text-gray-600 mb-1">
                      <FileText className="h-4 w-4" />
                      <span className="text-sm font-medium">Special Instructions</span>
                    </div>
                    <p className="text-sm text-gray-700">{order.special_instructions}</p>
                  </div>
                )}
                
                <div className="flex justify-end space-x-3">
                  <Link
                    href={`/orders/${order.id}`}
                    className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                  >
                    View Details
                  </Link>
                  <Link
                    href={`/orders/${order.id}/bill`}
                    className="text-green-600 hover:text-green-800 text-sm font-medium"
                  >
                    View Bill
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
} 