import React from 'react';

export default function HrPageHeader({ title, description, icon: Icon }) {
  return (
    <div className="flex items-center gap-4 mb-4">
      {Icon && (
        <div className="p-3 bg-blue-100 text-blue-600 rounded-xl">
          <Icon size={24} />
        </div>
      )}
      <div>
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">{title}</h1>
        {description && <p className="text-sm text-slate-500 mt-1">{description}</p>}
      </div>
    </div>
  );
}
