export interface User {
  id: number;
  name?: string;
  phone: string;
  is_verified: boolean;
  created_at: string;
}

export interface Restaurant {
  id: number;
  name: string;
  logo_url?: string;
  banner_url?: string;
  description?: string;
  address?: string;
  phone?: string;
  email?: string;
  created_at: string;
  updated_at?: string;
}

export interface MenuItem {
  id: number;
  name: string;
  short_description?: string;
  long_description?: string;
  price: number;
  image_url?: string;
  is_available: boolean;
  category?: string;
  restaurant_id: number;
  created_at: string;
  updated_at?: string;
}

export interface CartItem {
  id: number;
  menu_item_id: number;
  quantity: number;
  price_at_time: number;
  created_at: string;
  menu_item?: MenuItem;
}

export interface Cart {
  id: number;
  user_id: number;
  items: CartItem[];
  total_items: number;
  subtotal: number;
  created_at: string;
  updated_at?: string;
}

export interface OrderItem {
  id: number;
  menu_item_id: number;
  quantity: number;
  price_at_time: number;
  total_price: number;
  created_at: string;
  menu_item?: MenuItem;
}

export interface Order {
  id: number;
  order_number: string;
  user_id: number;
  subtotal: number;
  cgst_amount: number;
  sgst_amount: number;
  gst_amount: number;
  total_amount: number;
  status: string;
  delivery_address?: string;
  special_instructions?: string;
  items: OrderItem[];
  created_at: string;
  updated_at?: string;
}

export interface Bill {
  order_number: string;
  order_date: string;
  restaurant_name: string;
  restaurant_address: string;
  customer_name: string;
  customer_phone: string;
  delivery_address?: string;
  items: {
    name: string;
    quantity: number;
    price: number;
    total: number;
  }[];
  subtotal: number;
  cgst_amount: number;
  sgst_amount: number;
  gst_amount: number;
  total_amount: number;
  status: string;
  special_instructions?: string;
} 