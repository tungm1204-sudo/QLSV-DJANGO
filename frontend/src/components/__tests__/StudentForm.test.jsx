import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import StudentForm from '../StudentForm';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Mock the hooks
vi.mock('../features/students/hooks', () => ({
  useCreateStudent: () => ({
    mutateAsync: vi.fn(),
    isPending: false,
  }),
  useUpdateStudent: () => ({
    mutateAsync: vi.fn(),
    isPending: false,
  }),
}));

// Mock Dialog components to avoid Portal issues in JSDOM
vi.mock('@/components/ui/dialog', () => ({
  Dialog: ({ children, open }) => (open ? <div data-testid="dialog">{children}</div> : null),
  DialogContent: ({ children }) => <div>{children}</div>,
  DialogHeader: ({ children }) => <div>{children}</div>,
  DialogTitle: ({ children }) => <div>{children}</div>,
  DialogTrigger: ({ children }) => <div>{children}</div>,
}));


const queryClient = new QueryClient();

const wrapper = ({ children }) => (
  <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
);

describe('StudentForm', () => {
  it('renders the form correctly for new student', () => {
    try {
      render(<StudentForm isOpen={true} setIsOpen={() => {}} />, { wrapper });
      // screen.debug();
      expect(screen.getByText('Thêm Sinh Viên')).toBeInTheDocument();
      expect(screen.getByLabelText(/Mã số sinh viên/i)).toBeInTheDocument();
    } catch (error) {
      console.error('Test Error:', error);
      throw error;
    }
  });

  it('updates input values on change', () => {
    try {
      render(<StudentForm isOpen={true} setIsOpen={() => {}} />, { wrapper });
      
      const mssvInput = screen.getByLabelText(/Mã số sinh viên/i);
      fireEvent.change(mssvInput, { target: { value: 'SV999', name: 'mssv' } });
      
      expect(mssvInput.value).toBe('SV999');
    } catch (error) {
      console.error('Test Error:', error);
      throw error;
    }
  });
});

