'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Layout from '@/components/Layout';
import { Order } from '@/types';
import api from '@/lib/api';
import toast from 'react-hot-toast';
import { MapPin, FileText, Clock } from 'lucide-react';
import Link from 'next/link';

export default function OrderDetailsPage() {
  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);
  const params = useParams();
  const orderId = params.id as string;

  useEffect(() => {
    fetchOrder();
  }, [orderId]);

  const fetchOrder = async () => {
    try {
      const response = await api.get(`/orders/${orderId}`);
      setOrder(response.data);
    } catch (error) {
      console.error('Error fetching order:', error);
      toast.error('Failed to load order details');
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

  if (!order) {
    return (
      <Layout>
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Order not found</h2>
          <p className="text-gray-600">The requested order could not be loaded.</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Order Details</h1>
          <Link
            href={`/orders/${order.id}/bill`}
            className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
          >
            View Bill
          </Link>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Order Information</h2>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="font-medium text-gray-700">Order Number:</span>
                  <span className="text-gray-900">{order.order_number}</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium text-gray-700">Order Date:</span>
                  <span className="text-gray-900">
                    {new Date(order.created_at).toLocaleDateString()}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium text-gray-700">Order Time:</span>
                  <span className="text-gray-900">
                    {new Date(order.created_at).toLocaleTimeString()}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="font-medium text-gray-700">Status:</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(order.status)}`}>
                    {order.status}
                  </span>
                </div>
              </div>
            </div>

            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Delivery Information</h2>
              {order.delivery_address && (
                <div className="flex items-start space-x-2 mb-3">
                  <MapPin className="h-5 w-5 text-gray-400 mt-0.5" />
                  <div>
                    <p className="font-medium text-gray-700">Delivery Address</p>
                    <p className="text-gray-900">{order.delivery_address}</p>
                  </div>
                </div>
              )}
              {order.special_instructions && (
                <div className="flex items-start space-x-2">
                  <FileText className="h-5 w-5 text-gray-400 mt-0.5" />
                  <div>
                    <p className="font-medium text-gray-700">Special Instructions</p>
                    <p className="text-gray-900">{order.special_instructions}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Order Items */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Order Items</h2>
          <div className="space-y-4">
            {order.items.map((item) => (
              <div key={item.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div className="flex items-center space-x-4">
                  {item.menu_item?.image_url && (
                    <img
                      src={item.menu_item.image_url}
                      alt={item.menu_item.name}
                      className="w-16 h-16 object-cover rounded-md"
                    />
                  )}
                  <div>
                    <h3 className="font-semibold text-gray-900">
                      {item.menu_item?.name || 'Unknown Item'}
                    </h3>
                    <p className="text-sm text-gray-600">
                      Quantity: {item.quantity} × ₹{item.price_at_time}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-gray-900">₹{item.total_price}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Bill Summary */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Bill Summary</h2>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-700">Subtotal:</span>
              <span className="font-medium">₹{order.subtotal}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-700">CGST (9%):</span>
              <span className="font-medium">₹{order.cgst_amount}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-700">SGST (9%):</span>
              <span className="font-medium">₹{order.sgst_amount}</span>
            </div>
            <div className="flex justify-between text-lg font-bold border-t pt-3">
              <span>Total Amount:</span>
              <span className="text-blue-600">₹{order.total_amount}</span>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
} 