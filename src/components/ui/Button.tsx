import type { ButtonHTMLAttributes } from 'react';

type Variant = 'primary' | 'secondary' | 'danger' | 'ghost';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
}

const variants: Record<Variant, string> = {
  primary:
    'bg-indigo-600 hover:bg-indigo-500 text-white',
  secondary:
    'bg-gray-700 hover:bg-gray-600 text-gray-100 border border-gray-600',
  danger:
    'bg-red-700/80 hover:bg-red-600 text-white',
  ghost:
    'text-gray-300 hover:bg-gray-700 hover:text-white',
};

export function Button({ variant = 'primary', className = '', ...rest }: ButtonProps) {
  return (
    <button
      {...rest}
      className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${variants[variant]} ${className}`}
    />
  );
}
