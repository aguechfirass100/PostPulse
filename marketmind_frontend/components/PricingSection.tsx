import { useState } from "react";
import Link from "next/link";
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardFooter, 
  CardHeader, 
  CardTitle 
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { 
  CheckCircle2, 
  CreditCard, 
  Landmark, 
  Wallet, 
//   Paypal,
  DollarSign, 
  AppleIcon 
} from "lucide-react";

export default function PricingSection() {
  const [billingCycle, setBillingCycle] = useState("monthly");

  type ButtonVariant = "default" | "destructive" | "outline" | "secondary" | "ghost" | "link";

    interface Plan {
    name: string;
    description: string;
    monthlyPrice: number;
    yearlyPrice: number;
    features: string[];
    buttonVariant: ButtonVariant;
    buttonText: string;
    isPopular?: boolean;
    }

  
  const plans: Plan[] = [
    {
      name: "Free",
      description: "For individuals just getting started",
      monthlyPrice: 0,
      yearlyPrice: 0,
      features: [
        "5 AI content generations/month",
        "2 social media accounts",
        "Basic analytics",
        "Limited image generation"
      ],
      buttonVariant: "outline",
      buttonText: "Sign Up Free"
    },
    {
      name: "Premium",
      description: "For content creators and influencers",
      monthlyPrice: 29,
      yearlyPrice: 290, // ~17% discount
      features: [
        "100 AI content generations/month",
        "5 social media accounts",
        "Advanced analytics",
        "50 image generations/month",
        "10 video generations/month"
      ],
      buttonVariant: "default",
      buttonText: "Choose Premium"
    },
    {
      name: "Business",
      description: "For small businesses and startups",
      monthlyPrice: 79,
      yearlyPrice: 790, // ~17% discount
      features: [
        "Unlimited AI content generations",
        "10 social media accounts",
        "Comprehensive analytics",
        "200 image generations/month",
        "50 video generations/month",
        "Sentiment analysis",
        "Basic trend prediction"
      ],
      buttonVariant: "default",
      buttonText: "Choose Business",
      isPopular: true
    },
    {
      name: "Business Plus",
      description: "For growing businesses and agencies",
      monthlyPrice: 199,
      yearlyPrice: 1990, // ~17% discount
      features: [
        "Everything in Business",
        "25 social media accounts",
        "Unlimited image generations",
        "200 video generations/month",
        "Advanced trend prediction",
        "Priority support"
      ],
      buttonVariant: "default",
      buttonText: "Choose Business Plus"
    },
    {
      name: "Pay As You Go",
      description: "For occasional users",
      monthlyPrice: 19,
      yearlyPrice: 190, // ~17% discount
      features: [
        "Base subscription + credits",
        "3 social media accounts",
        "$10 = 50 text generations",
        "$15 = 25 image generations",
        "$20 = 10 video generations"
      ],
      buttonVariant: "outline",
      buttonText: "Choose Pay As You Go"
    }
  ];

  return (
    <section id="pricing" className="py-20 px-4 bg-gradient-to-b from-gray-50 to-white dark:from-gray-950 dark:to-gray-900">
      <div className="container max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Flexible Plans for Every Need</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Choose the plan that works best for you, from freelancers to enterprise businesses.
          </p>
          
          {/* Billing toggle */}
          <div className="flex items-center justify-center mt-8 space-x-4">
            <span className={`text-sm font-medium ${billingCycle === "monthly" ? "text-primary" : "text-muted-foreground"}`}>
              Monthly
            </span>
            <Switch
              checked={billingCycle === "yearly"}
              onCheckedChange={(checked) => setBillingCycle(checked ? "yearly" : "monthly")}
              className="data-[state=checked]:bg-primary"
            />
            <div className="flex items-center">
              <span className={`text-sm font-medium ${billingCycle === "yearly" ? "text-primary" : "text-muted-foreground"}`}>
                Yearly
              </span>
              <span className="ml-2 inline-block bg-green-100 text-green-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-green-900 dark:text-green-100">
                Save 17%
              </span>
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-8">
          {plans.map((plan, index) => (
            <Card 
              key={index}
              className={`relative overflow-hidden border ${plan.isPopular ? 'border-2 border-primary shadow-lg' : 'shadow-sm'} rounded-xl hover:shadow-md transition-all duration-300 ${plan.isPopular ? 'scale-105' : ''}`}
            >
              {plan.isPopular && (
                <div className="absolute top-0 right-0">
                  <div className="bg-primary text-primary-foreground text-xs font-medium px-4 py-1 rounded-bl-lg">
                    POPULAR
                  </div>
                </div>
              )}
              <CardHeader className="pb-2">
                <CardTitle className="text-2xl">{plan.name}</CardTitle>
                <CardDescription className="text-sm">{plan.description}</CardDescription>
                <div className="mt-4 flex items-end">
                  <span className="text-4xl font-bold">
                    ${billingCycle === "monthly" ? plan.monthlyPrice : plan.yearlyPrice}
                  </span>
                  <span className="text-muted-foreground ml-1 text-sm">
                    /{billingCycle === "monthly" ? "month" : "year"}
                  </span>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3 text-sm mb-6">
                  {plan.features.map((feature, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-primary mt-0.5 flex-shrink-0" />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
              <CardFooter className="flex flex-col space-y-4">
                <Button className="w-full" variant={plan.buttonVariant} asChild>
                  <Link href="/signup">{plan.buttonText}</Link>
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>

        {/* Payment methods */}
        <div className="mt-16 pt-8 border-t border-gray-200 dark:border-gray-800">
          <div className="text-center mb-8">
            <h3 className="text-xl font-semibold mb-2">Accepted Payment Methods</h3>
            <p className="text-muted-foreground">Secure and flexible payment options for your convenience</p>
          </div>
          
          <div className="flex flex-wrap justify-center items-center gap-8">
            <div className="flex items-center gap-2 text-muted-foreground">
              <CreditCard className="w-6 h-6" />
              <span>Credit Card</span>
            </div>
            <div className="flex items-center gap-2 text-muted-foreground">
              <DollarSign className="w-6 h-6" />
              <span>PayPal</span>
            </div>
            <div className="flex items-center gap-2 text-muted-foreground">
              <Landmark className="w-6 h-6" />
              <span>Bank Transfer</span>
            </div>
            <div className="flex items-center gap-2 text-muted-foreground">
              <AppleIcon className="w-6 h-6" />
              <span>Apple Pay</span>
            </div>
            <div className="flex items-center gap-2 text-muted-foreground">
              <Wallet className="w-6 h-6" />
              <span>Crypto</span>
            </div>
          </div>
        </div>

        <div className="mt-12 text-center">
          <p className="text-muted-foreground">
            Need a custom solution for your enterprise? <Link href="/contact" className="text-primary hover:underline">Contact us</Link> for custom pricing.
          </p>
        </div>
      </div>
    </section>
  );
}