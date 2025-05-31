export interface Portfolio {
    id: string;
    name: string;
    stocks: Array<{
      stockId: string;
      quantity: number;
    }>;
    createdAt: Date;
    updatedAt: Date;
  }
  