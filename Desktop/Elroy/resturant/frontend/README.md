# Restaurant Frontend

Next.js frontend for the restaurant menu and ordering system with modern UI, OTP authentication, and responsive design.

## Features

- **Modern UI**: Responsive design with Tailwind CSS
- **OTP Authentication**: Phone-based login flow
- **Menu Browsing**: Category filtering and item details
- **Shopping Cart**: Quantity management and cart operations
- **Order Management**: Order history and detailed views
- **Bill Display**: Printable bills with GST breakdown
- **Production Optimized**: TypeScript, ESLint, optimized builds

## Tech Stack

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **React Hot Toast**: Notifications
- **Lucide React**: Icons
- **React Context**: State management

## Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Development Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API URL
   ```

4. **Run development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   - Frontend: http://localhost:3000

### Production Build

1. **Build the application:**
   ```bash
   npm run build
   ```

2. **Start production server:**
   ```bash
   npm start
   ```

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # App Router pages
│   │   ├── page.tsx           # Home page
│   │   ├── login/             # Authentication
│   │   ├── menu/              # Menu browsing
│   │   ├── cart/              # Shopping cart
│   │   ├── checkout/          # Order placement
│   │   └── orders/            # Order management
│   ├── components/            # React components
│   │   ├── Layout.tsx         # Main layout
│   │   └── Bill.tsx           # Bill component
│   ├── hooks/                 # Custom hooks
│   │   └── useAuth.ts         # Authentication hook
│   ├── lib/                   # Utilities
│   │   └── api.ts             # API client
│   └── types/                 # TypeScript types
│       └── index.ts           # Type definitions
├── public/                    # Static assets
├── package.json               # Dependencies
└── next.config.js            # Next.js config
```

## Pages

### Home Page (`/`)
- Restaurant information and branding
- Featured menu items
- Call-to-action to browse menu

### Login Page (`/login`)
- Phone number input
- OTP verification
- Authentication state management

### Menu Page (`/menu`)
- Menu items with images and descriptions
- Category filtering
- Add to cart functionality
- Quantity selection

### Cart Page (`/cart`)
- Cart items display
- Quantity updates
- Remove items
- Order summary
- Proceed to checkout

### Checkout Page (`/checkout`)
- Delivery address input
- Special instructions
- Order summary with GST
- Place order functionality

### Orders Page (`/orders`)
- Order history
- Order status tracking
- Order details view
- Bill generation

## Components

### Layout Component
Main layout wrapper with:
- Header with navigation
- User authentication status
- Cart icon
- Responsive design

### Bill Component
Printable bill with:
- Restaurant branding
- Order details
- Item breakdown
- GST calculation
- Print functionality

## Hooks

### useAuth Hook
Authentication state management:
- User login/logout
- Token management
- User data persistence
- Authentication status

## API Integration

### API Client (`lib/api.ts`)
Axios-based HTTP client with:
- Base URL configuration
- Request/response interceptors
- Authentication token handling
- Error handling

### API Endpoints
- Authentication: `/api/v1/auth/*`
- Menu: `/api/v1/menu/*`
- Cart: `/api/v1/cart/*`
- Orders: `/api/v1/orders/*`

## State Management

### Authentication State
- User information
- Login status
- Token management
- Local storage persistence

### Cart State
- Cart items
- Quantities
- Price calculations
- API synchronization

## Styling

### Tailwind CSS
- Utility-first approach
- Responsive design
- Custom color scheme
- Component-based styling

### Design System
- Color palette
- Typography
- Spacing
- Component variants

## Environment Variables

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Optional: Analytics
NEXT_PUBLIC_GA_ID=your-google-analytics-id
```

## Development

### Code Quality
```bash
# Lint code
npm run lint

# Type checking
npm run type-check

# Format code
npm run format
```

### Testing
```bash
# Run tests
npm test

# Run with coverage
npm run test:coverage
```

### Build Optimization
```bash
# Analyze bundle
npm run build:analyze

# Export static site
npm run export
```

## Performance Optimizations

### Next.js Optimizations
- App Router for better performance
- Automatic code splitting
- Image optimization
- Static generation where possible

### React Optimizations
- Memoization with React.memo
- Custom hooks for logic reuse
- Efficient re-renders
- Lazy loading

### Bundle Optimizations
- Tree shaking
- Code splitting
- Dynamic imports
- Bundle analysis

## SEO and Meta Tags

### Dynamic Meta Tags
- Page-specific titles
- Open Graph tags
- Twitter cards
- Structured data

### Performance Metrics
- Core Web Vitals
- Lighthouse scores
- Bundle size monitoring
- Loading performance

## Accessibility

### ARIA Labels
- Screen reader support
- Keyboard navigation
- Focus management
- Semantic HTML

### Color Contrast
- WCAG compliance
- High contrast mode
- Color-blind friendly
- Readable typography

## Error Handling

### Global Error Boundary
- Catch JavaScript errors
- Fallback UI
- Error reporting
- User-friendly messages

### API Error Handling
- Network errors
- Authentication errors
- Validation errors
- Server errors

## Security

### Authentication
- JWT token storage
- Secure token handling
- Automatic token refresh
- Logout functionality

### Input Validation
- Client-side validation
- API validation
- XSS prevention
- CSRF protection

## Deployment

### Vercel (Recommended)
1. Connect GitHub repository
2. Configure environment variables
3. Deploy automatically

### Netlify
1. Build command: `npm run build`
2. Publish directory: `out`
3. Configure redirects

### Local Production
```bash
# Build the application
npm run build

# Start production server
npm start
```

## Monitoring

### Error Tracking
- Sentry integration
- Error boundaries
- Performance monitoring
- User analytics

### Analytics
- Google Analytics
- Custom events
- User behavior
- Conversion tracking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run linting and formatting
6. Submit a pull request

## Development Guidelines

### Code Style
- TypeScript strict mode
- ESLint configuration
- Prettier formatting
- Consistent naming

### Component Structure
- Functional components
- Custom hooks for logic
- Props interface
- Default exports

### File Organization
- Feature-based structure
- Shared components
- Utility functions
- Type definitions

## Troubleshooting

### Common Issues
- API connection errors
- Authentication problems
- Build failures
- Performance issues

### Debug Tools
- React DevTools
- Network tab
- Console logging
- Error boundaries

## License

This project is licensed under the MIT License.
