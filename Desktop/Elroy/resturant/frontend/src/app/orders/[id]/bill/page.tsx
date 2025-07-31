'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Layout from '@/components/Layout';
import BillComponent from '@/components/Bill';
import { Bill } from '@/types';
import api from '@/lib/api';
import toast from 'react-hot-toast';

export default function BillPage() {
  const [bill, setBill] = useState<Bill | null>(null);
  const [loading, setLoading] = useState(true);
  const params = useParams();
  const orderId = params.id as string;

  useEffect(() => {
    fetchBill();
  }, [orderId]);

  const fetchBill = async () => {
    try {
      const response = await api.get(`/orders/${orderId}/bill`);
      setBill(response.data);
    } catch (error) {
      console.error('Error fetching bill:', error);
      toast.error('Failed to load bill');
    } finally {
      setLoading(false);
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

  if (!bill) {
    return (
      <Layout>
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Bill not found</h2>
          <p className="text-gray-600">The requested bill could not be loaded.</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <BillComponent bill={bill} />
    </Layout>
  );
} 