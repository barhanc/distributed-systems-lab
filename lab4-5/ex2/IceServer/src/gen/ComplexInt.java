//
// Copyright (c) ZeroC, Inc. All rights reserved.
//
//
// Ice version 3.7.10
//
// <auto-generated>
//
// Generated from file `Complex.ice'
//
// Warning: do not edit this file.
//
// </auto-generated>
//

package gen;

public class ComplexInt implements java.lang.Cloneable,
                                   java.io.Serializable
{
    public int re;

    public int im;

    public ComplexInt()
    {
    }

    public ComplexInt(int re, int im)
    {
        this.re = re;
        this.im = im;
    }

    public boolean equals(java.lang.Object rhs)
    {
        if(this == rhs)
        {
            return true;
        }
        ComplexInt r = null;
        if(rhs instanceof ComplexInt)
        {
            r = (ComplexInt)rhs;
        }

        if(r != null)
        {
            if(this.re != r.re)
            {
                return false;
            }
            if(this.im != r.im)
            {
                return false;
            }

            return true;
        }

        return false;
    }

    public int hashCode()
    {
        int h_ = 5381;
        h_ = com.zeroc.IceInternal.HashUtil.hashAdd(h_, "::Complex::ComplexInt");
        h_ = com.zeroc.IceInternal.HashUtil.hashAdd(h_, re);
        h_ = com.zeroc.IceInternal.HashUtil.hashAdd(h_, im);
        return h_;
    }

    public ComplexInt clone()
    {
        ComplexInt c = null;
        try
        {
            c = (ComplexInt)super.clone();
        }
        catch(CloneNotSupportedException ex)
        {
            assert false; // impossible
        }
        return c;
    }

    public void ice_writeMembers(com.zeroc.Ice.OutputStream ostr)
    {
        ostr.writeInt(this.re);
        ostr.writeInt(this.im);
    }

    public void ice_readMembers(com.zeroc.Ice.InputStream istr)
    {
        this.re = istr.readInt();
        this.im = istr.readInt();
    }

    static public void ice_write(com.zeroc.Ice.OutputStream ostr, ComplexInt v)
    {
        if(v == null)
        {
            _nullMarshalValue.ice_writeMembers(ostr);
        }
        else
        {
            v.ice_writeMembers(ostr);
        }
    }

    static public ComplexInt ice_read(com.zeroc.Ice.InputStream istr)
    {
        ComplexInt v = new ComplexInt();
        v.ice_readMembers(istr);
        return v;
    }

    static public void ice_write(com.zeroc.Ice.OutputStream ostr, int tag, java.util.Optional<ComplexInt> v)
    {
        if(v != null && v.isPresent())
        {
            ice_write(ostr, tag, v.get());
        }
    }

    static public void ice_write(com.zeroc.Ice.OutputStream ostr, int tag, ComplexInt v)
    {
        if(ostr.writeOptional(tag, com.zeroc.Ice.OptionalFormat.VSize))
        {
            ostr.writeSize(8);
            ice_write(ostr, v);
        }
    }

    static public java.util.Optional<ComplexInt> ice_read(com.zeroc.Ice.InputStream istr, int tag)
    {
        if(istr.readOptional(tag, com.zeroc.Ice.OptionalFormat.VSize))
        {
            istr.skipSize();
            return java.util.Optional.of(ComplexInt.ice_read(istr));
        }
        else
        {
            return java.util.Optional.empty();
        }
    }

    private static final ComplexInt _nullMarshalValue = new ComplexInt();

    /** @hidden */
    public static final long serialVersionUID = -8104108651895490517L;
}