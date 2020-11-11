program fdtd
    implicit none
    integer, parameter :: length=240, number_of_frames=60, steps_per_frame=12
    integer :: k, frame, step
    real, dimension(length) :: epsilon_r, mu_r, mE, mH, Ey, Hx
    real, dimension(number_of_frames*steps_per_frame) :: source
    real :: dz=1, dt=1
    character(len=20) :: filename, format_string

    do k=1, length
        ! Initialize materials to free space
        epsilon_r(k)=1
        mu_r(k)=1

        ! Initialize fields to zero
        Hx(k)=0
        Ey(k)=0
    end do

    ! Generate source
    do step=1, number_of_frames*steps_per_frame
        source(step)= exp(-((step*dt-40)/10)**2)
    end do


    ! Compute update coefficients
    mE = 0.5/epsilon_r
    mH = 0.5/mu_r
    
    ! dt = n*dz/(2*c0)
    ! n := refractive index at boundries
    ! mE = c0*dt/epsilon_r = n*dz/(2*epsilon_r)
    ! mH = c0*dt/mu_r = n*dz/(2*mu_r)


    ! Format for output
    format_string = 'E16.9'

    ! ---------------- Main FDTD loop ---------------- 
    do frame = 1, number_of_frames

        ! Generate filename with frame number
        write (filename,'(I4.4".csv")') frame

        ! Write Hx to a CSV file
        open(1, file='./output/Hx'//filename, status='replace')
        do k = 1, length-1
            write(1,'('//format_string//'",")',advance='NO') Hx(k)
        end do
        write(1,'('//format_string//')',advance='NO') Hx(length)
        close(1)

        ! Write Ey to a CSV file
        open(2, file='./output/Ey'//filename, status='replace')
        write(2,'('//format_string//')',advance='NO') Ey(1)
        do k = 2, length
            write(2,'(","'//format_string//')',advance='NO') Ey(k)
        end do
        close(2)


        ! Run simulation up to next frame
        do step = 1, steps_per_frame
            ! Update Hx
            do k = 1, length-1
                Hx(k) = Hx(k) + mH(k)*(Ey(k+1)-Ey(k))/dz
            end do
            Hx(length) = Hx(length) - mH(length)*Ey(length)/dz

            ! Update Ey
            Ey(1) = Ey(1) + mE(1)*Hx(1)/dz
            do k = 2, length
                Ey(k) = Ey(k) + mE(k)*(Hx(k)-Hx(k-1))/dz
            end do

            ! Inject source
            Ey(60) = Ey(60) + source(step + (frame-1)*steps_per_frame)

        end do

    end do


end program fdtd