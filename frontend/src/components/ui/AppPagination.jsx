import React from 'react';
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination';

export default function AppPagination({ page, setPage, count, pageSize = 10 }) {
  const totalPages = Math.ceil(count / pageSize) || 1;

  if (count === 0) return null;

  return (
    <div className="flex items-center justify-between mt-4 pb-2">
      <div className="text-sm text-slate-500">
        Hiển thị {Math.min((page - 1) * pageSize + 1, count)} - {Math.min(page * pageSize, count)} trong số {count} kết quả
      </div>
      <Pagination className="justify-end w-auto mx-0">
        <PaginationContent>
          <PaginationItem>
            <PaginationPrevious 
              href="#" 
              onClick={(e) => {
                e.preventDefault();
                if (page > 1) setPage(page - 1);
              }}
              className={page <= 1 ? "pointer-events-none opacity-50" : ""}
            />
          </PaginationItem>
          
          {[...Array(totalPages)].map((_, i) => {
            const pageNum = i + 1;
            // Hiển thị các trang gần trang hiện tại, trang đầu và trang cuối
            if (
              pageNum === 1 || 
              pageNum === totalPages ||
              (pageNum >= page - 1 && pageNum <= page + 1)
            ) {
              return (
                <PaginationItem key={pageNum}>
                  <PaginationLink 
                    href="#" 
                    isActive={page === pageNum}
                    onClick={(e) => {
                      e.preventDefault();
                      setPage(pageNum);
                    }}
                  >
                    {pageNum}
                  </PaginationLink>
                </PaginationItem>
              );
            } else if (
              pageNum === page - 2 || 
              pageNum === page + 2
            ) {
              return <PaginationItem key={pageNum}><span className="px-2">...</span></PaginationItem>;
            }
            return null;
          })}

          <PaginationItem>
            <PaginationNext 
              href="#" 
              onClick={(e) => {
                e.preventDefault();
                if (page < totalPages) setPage(page + 1);
              }}
              className={page >= totalPages ? "pointer-events-none opacity-50" : ""}
            />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    </div>
  );
}
