export const currencySymbols: Record<string, string> = {
    USD: '$',
    GBP: '£',
    EUR: '€',
    JPY: '¥',
    CAD: 'C$',
    AUD: 'A$',
};

export function formatPrice(amount: number, currency: string): string {
    const symbol = currencySymbols[currency] || currency + ' ';
    return `${symbol}${amount.toFixed(2)}`;
}
