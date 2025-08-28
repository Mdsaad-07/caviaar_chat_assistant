// pages/index.tsx  (or app/page.tsx if you’re using the App Router)

import Head from 'next/head';
import dynamic from 'next/dynamic';

// 👉  Disable SSR for the chat widget
const CaviaarModeChat = dynamic(() => import('../components/Chat'), {
  ssr: false,
  // (optional) small loading fallback
  loading: () => null,
});

export default function Home() {
  return (
    <>
      <Head>
        <title>Caviaar Mode - AI Shopping Assistant</title>
        <meta
          name="description"
          content="Smart AI assistant for Caviaar Mode fashion store"
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        {/* Demo Content */}
        <div className="container mx-auto px-4 py-16">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Caviaar Mode AI Assistant
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Experience our intelligent shopping assistant that helps with
              products, sizing, payments, returns, and shipping inquiries.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <div className="bg-white p-6 rounded-xl shadow-sm border">
              <h3 className="font-semibold text-lg mb-3">Product Assistance</h3>
              <p className="text-gray-600">
                Get personalized product recommendations and detailed
                information about our collections.
              </p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm border">
              <h3 className="font-semibold text-lg mb-3">Size Guidance</h3>
              <p className="text-gray-600">
                Find the perfect fit with our comprehensive size guides for all
                product categories.
              </p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm border">
              <h3 className="font-semibold text-lg mb-3">Order Support</h3>
              <p className="text-gray-600">
                Track orders, process returns, and get help with payments and
                shipping.
              </p>
            </div>
          </div>

          <div className="text-center mt-12">
            <p className="text-gray-500">
              👉 Try the AI assistant in the bottom-right corner
            </p>
          </div>
        </div>

        {/* Chat widget (client-only) */}
        <CaviaarModeChat />
      </main>
    </>
  );
}
