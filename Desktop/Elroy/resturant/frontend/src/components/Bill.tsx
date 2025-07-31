import { Bill } from '@/types';
import { Printer } from 'lucide-react';

interface BillProps {
  bill: Bill;
}

export default function BillComponent({ bill }: BillProps) {
  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-sm p-8 print:shadow-none">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          {bill.restaurant_name}
        </h1>
        {bill.restaurant_address && (
          <p className="text-gray-600 text-sm">{bill.restaurant_address}</p>
        )}
        <div className="mt-4 text-sm text-gray-500">
          <p>Order Date: {new Date(bill.order_date).toLocaleDateString()}</p>
          <p>Order Time: {new Date(bill.order_date).toLocaleTimeString()}</p>
        </div>
      </div>

      {/* Order Details */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Order Details</h2>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="font-medium">Order Number:</span>
            <span>{bill.order_number}</span>
          </div>
          <div className="flex justify-between">
            <span className="font-medium">Customer Name:</span>
            <span>{bill.customer_name}</span>
          </div>
          <div className="flex justify-between">
            <span className="font-medium">Phone:</span>
            <span>{bill.customer_phone}</span>
          </div>
          {bill.delivery_address && (
            <div className="flex justify-between">
              <span className="font-medium">Delivery Address:</span>
              <span className="text-right max-w-xs">{bill.delivery_address}</span>
            </div>
          )}
          <div className="flex justify-between">
            <span className="font-medium">Status:</span>
            <span className="capitalize">{bill.status}</span>
          </div>
        </div>
      </div>

      {/* Items */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Order Items</h2>
        <div className="border-t border-b border-gray-200">
          {bill.items.map((item, index) => (
            <div key={index} className="py-3 border-b border-gray-100 last:border-b-0">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{item.name}</p>
                  <p className="text-sm text-gray-600">Quantity: {item.quantity}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-600">₹{item.price} each</p>
                  <p className="font-semibold text-gray-900">₹{item.total}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Bill Summary */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Bill Summary</h2>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span>Subtotal:</span>
            <span>₹{bill.subtotal}</span>
          </div>
          <div className="flex justify-between">
            <span>CGST (9%):</span>
            <span>₹{bill.cgst_amount}</span>
          </div>
          <div className="flex justify-between">
            <span>SGST (9%):</span>
            <span>₹{bill.sgst_amount}</span>
          </div>
          <div className="flex justify-between font-bold text-lg border-t pt-2">
            <span>Total Amount:</span>
            <span className="text-blue-600">₹{bill.total_amount}</span>
          </div>
        </div>
      </div>

      {/* Special Instructions */}
      {bill.special_instructions && (
        <div className="mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">Special Instructions</h2>
          <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded">
            {bill.special_instructions}
          </p>
        </div>
      )}

      {/* Footer */}
      <div className="text-center text-sm text-gray-500 border-t pt-6">
        <p>Thank you for your order!</p>
        <p className="mt-2">This is a demo application. No actual payment is required.</p>
      </div>

      {/* Print Button */}
      <div className="mt-6 text-center print:hidden">
        <button
          onClick={handlePrint}
          className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 flex items-center space-x-2 mx-auto"
        >
          <Printer className="h-4 w-4" />
          <span>Print Bill</span>
        </button>
      </div>
    </div>
  );
} 