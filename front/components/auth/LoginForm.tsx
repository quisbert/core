"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import { Eye, EyeOff, Loader2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { useAuthStore } from "@/stores/auth.store";
import { useAppStore } from "@/stores/app.store";

import {
  loginSchema,
  type LoginForm,
} from "@/validators/auth";

export default function LoginForm() {
  const router = useRouter();

  const [showPassword, setShowPassword] =
    useState(false);

  const {
    signIn,
    error,
    clearError,
    isLoading,
  } = useAuthStore();

  const {
    organization,
    load,
  } = useAppStore();

  useEffect(() => {
    load();
  }, [load]);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (
    values: LoginForm,
  ) => {
    clearError();

    try {
      await signIn(values);
      router.push("/dashboard");
    } catch {}
  };

  return (
    <Card className="w-full max-w-md shadow-xl">

      <CardHeader>

        <CardTitle>
          {organization?.system_name ??
            "Core API"}
        </CardTitle>

        <CardDescription>
          {organization?.login_message ??
            "Enter your credentials to continue."}
        </CardDescription>

      </CardHeader>

      <CardContent>

        <form
          onSubmit={handleSubmit(onSubmit)}
          className="space-y-5"
        >

          <div className="space-y-2">

            <Label>
              Username
            </Label>

            <Input
              placeholder="Username"
              {...register("username")}
            />

            {errors.username && (
              <p className="text-sm text-destructive">
                {errors.username.message}
              </p>
            )}

          </div>

          <div className="space-y-2">

            <Label>
              Password
            </Label>

            <div className="relative">

              <Input
                type={
                  showPassword
                    ? "text"
                    : "password"
                }
                placeholder="Password"
                {...register("password")}
              />

              <button
                type="button"
                onClick={() =>
                  setShowPassword(
                    !showPassword,
                  )
                }
                className="absolute right-3 top-1/2 -translate-y-1/2"
              >
                {showPassword ? (
                  <EyeOff className="h-4 w-4" />
                ) : (
                  <Eye className="h-4 w-4" />
                )}
              </button>

            </div>

            {errors.password && (
              <p className="text-sm text-destructive">
                {errors.password.message}
              </p>
            )}

          </div>

          {error && (
            <div className="rounded-md border border-destructive bg-destructive/10 p-3 text-sm text-destructive">
              {error}
            </div>
          )}

          <Button
            type="submit"
            className="w-full"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Signing in...
              </>
            ) : (
              "Sign in"
            )}
          </Button>

        </form>

      </CardContent>

    </Card>
  );
}