import React from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { EnhancerPage } from "./pages/EnhancerPage";

const queryClient = new QueryClient();

const App: React.FC = () => (
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<EnhancerPage />} />
      </Routes>
    </BrowserRouter>
  </QueryClientProvider>
);

export default App;
